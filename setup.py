import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="mongodb-sentry-integration",
    version="1.0.0",
    description="A integration of MongoDB for the Sentry's Python SDK",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/JoeVictor22/mongo_integration_sentry_python_sdk",
    author="Joel Castro",
    author_email="joelvictor1746@gmail.com",
    license="MIT",
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    packages=["sentry_mongo"],
    include_package_data=True,
    install_requires=["sentry_sdk~=1.5", "pymongo~=3.12"],
)
