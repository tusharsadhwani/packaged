# packaged

The easiest way to ship python applications.

## Installation

```bash
pip install packaged
```

## Usage

```bash
packaged <source_directory> <build_command> <startup_command>
```

For example:

```bash
packaged path/to/project.py 'pip install .' 'python -m your_package'
```

## Local Development / Testing

- Create and activate a virtual environment
- Run `pip install -r requirements-dev.txt` to do an editable install
- Run `pytest` to run tests

## Type Checking

Run `mypy .`

## Create and upload a package to PyPI

Make sure to bump the version in `setup.cfg`.

Then run the following commands:

```bash
rm -rf build dist
python setup.py sdist bdist_wheel
```

Then upload it to PyPI using [twine](https://twine.readthedocs.io/en/latest/#installation):

```bash
twine upload dist/*
```
