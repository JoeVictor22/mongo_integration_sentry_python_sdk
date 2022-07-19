# mongodb-sentry-integration
Integration of MongoDB for the Sentry's Python SDK.

Check on [pypi](https://pypi.org/project/mongodb-sentry-integration/)

### Install

```shell
pip install mongodb-sentry-integration
```

### Configuration

```python
import sentry_sdk
from sentry_mongo.integrations import MongoIntegration

sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    integrations=[
        MongoIntegration(),
    ],
)
```

### Usage

- TODO
