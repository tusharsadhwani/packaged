# packaged

The easiest way to ship python applications.

## Installation

```bash
pip install packaged
```

## Usage

```bash
packaged <output_path> <build_command> <startup_command> [<source_directory>]
```

Such as:

```bash
packaged my_project.bin 'pip install .' 'python -m your_package' path/to/project
```

## Examples

All examples below create a self contained executable. You can send the produced
binary file to another machine with the same OS and architecture, and it will
run the same.

### Graphs / matplotlib

```bash
packaged ./curve.bin 'pip install -r requirements.txt' 'python bubble_sort_curve.py' ./example/matplotlib
```

This produces a `./curve.bin` binary with:

- Python 3.11
- `matplotlib`
- `numba`
- `llvmlite`
- `pillow`

That outputs an interactive graph GUI.

### Minesweeper (using `packaged.toml` for configuration)

You can use a `packaged.toml` file and simply do `packaged path/to/project` to
create your package. For example, try the `minesweeper` project:

```bash
packaged ./example/minesweeper
```

[This configuration](tests/end_to_end/test_packages/minesweeper/packaged.toml)
is used for building the package. The equivalent command to build the project
without `pyproject.toml` would be:

```bash
packaged minesweeper.bin 'pip install .' 'python -m minesweeper' ./example/minesweeper
```

### Textual Demo

Since the dependencies themselves contain all the source code needed, you can
skip the last argument. With this, no other files will be packaged other than
what is produced in the build step.

```bash
packaged './textualdemo.bin' 'pip install textual' 'python -m textual'
```

This will simply package the `textual` library's own demo into a single file.

### Chimp game (pygame)

Pygame ships with various games as well, `pygame.examples.chimp` is one of them:

```bash
packaged './chimp' 'pip install pygame' 'python -m pygame.examples.chimp'
```

Another fun game that you can try out are `pygame.examples.aliens`.

## Local Development / Testing

To test and modify the package locally:

- Create and activate a virtual environment
- Run `pip install -r requirements-dev.txt` to do an editable install
- Run `pytest` to run tests
- Make changes as needed

### Type Checking

Run `mypy .`

### Create and upload a package to PyPI

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
