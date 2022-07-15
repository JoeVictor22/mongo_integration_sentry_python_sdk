from pymongo import monitoring
import sentry_sdk
from sentry_sdk.integrations import Integration


class MongoIntegration(Integration):
    """
    The sentry_sdk integration of MongoDB.
    """

    identifier = "mongodb"

    @staticmethod
    def setup_once():
        monitoring.register(MongoCommandListener())


class MongoCommandListener(monitoring.CommandListener):
    """
    Create spans using Mongo command listener.

    This class handles and store the context of spans, at each executed mongo command we create
    a new span and store it for later use. At the end of the command life, we retrieve this span and close it.
    """

    _commands_to_listen = ["updates", "deletes", "documents"]
    _operations_to_listen = ["filter", "limit", "sort", "skip", "pipeline", "query"]
    """
    These are the type of mongo commands/operators that are gonna to be written to a span.
    The _commands_to_listen refers to commands that involves tampering with multiple objets.
    The _operations_to_listen refers to operations in general that we want to have information saved.
    We made this bit so we can keep track of the number of documents affected by the _commands_to_listen,
    while _operations_to_listen we wanted to store individual information of any operator involved in the command,
    e.g. how many objects to limit.
    """

    def __init__(self):
        self._spans = dict()
        """
        Make sure that every class instance has it's own dict of spans;
        Keys on this dict should represent the event.request_id object;
        """

    def started(self, event):
        """
        Here we gather info about the event, create a new span and store it on memory.
        """

        def get_span(event):
            cmd_type = str(event.command_name)
            command = str(event.command.get(cmd_type))
            description = f"mongodb.{command}.{cmd_type}"
            data = {}

            """Builds span description"""
            for atr in self._operations_to_listen:
                value = event.command.get(atr)
                if value is not None:
                    data[atr] = str(value)
                    description += f".{atr}"

            if event.command.get("collection"):
                """Concatenates collection name to description"""
                data["collection"] = str(event.command["collection"])
                description += f".{data['collection']}"

            for atr in self._commands_to_listen:
                """Gather information about the number of documents affected"""
                value = event.command.get(atr)
                if value is not None:
                    data[f"number of documents affected by {atr}"] = len(value)
                    data[atr] = str(value)

            span = sentry_sdk.start_span(op="mongodb", description=description)

            """Add tags to the span"""
            span.set_tag("db.type", "mongodb")
            span.set_tag("db.instance", str(event.database_name))
            span.set_tag("db.statement", command)
            span.set_tag("request_id", str(event.request_id))
            span.set_tag("connection_id", str(event.connection_id))

            for k, v in data.items():
                """Append our gathered data to the span"""
                span.set_data(k, v)
            return span

        span = get_span(event)
        span = span.__enter__()

        if span is not None:
            """Save the span in memory so we can latter use it"""
            self._spans[event.request_id] = span

    def succeeded(self, event):
        self._stop("ok", event)

    def failed(self, event):
        self._stop("internal_error", event)

    def _stop(self, status, event):
        """Finishes span context and removes it from the memory"""
        span = self._spans.get(event.request_id, None)
        if span is not None:
            span.set_status(status)
            span.__exit__(None, None, None)
            del self._spans[event.request_id]


if __name__ == "__main__":
    pass
