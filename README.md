# packaged

The easiest way to ship python applications.

## Installation

```bash
pip install packaged
```

## Usage

```bash
packaged <source_directory> <output_file> <build_command> <startup_command>
```

Such as:

```bash
packaged path/to/project my_project.bin 'pip install .' 'python -m your_package'
```

### Example

There's an `example` folder where you can test this:

```bash
pip install packaged
cd example
packaged . curve 'pip install -r requirements.txt' 'python bubble_sort_curve.py'
```

This produces a `./curve` binary with:

- Python 3.11
- `matplotlib`
- `numba`
- `llvmlite`
- `pillow`

... and is directly executable. You can send this binary file to another machine
with the same OS and architecture, and it will run the same.

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
