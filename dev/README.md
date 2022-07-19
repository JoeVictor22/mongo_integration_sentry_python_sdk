
### Installing package

#### Pip

```shell
python -m pip install -e .
```

#### Egg-info

```shell
python setup.py egg_info
pip install -r mongodb_sentry_integration.egg-info/requires.txt 
```

### Build package

```shell
python -m build

# rename .whl to .zip and check contents or use twine to check contents
twine check dist/*
```

### Upload
```shell
# upload to testpypi
twine upload -r testpypi dist/*

```