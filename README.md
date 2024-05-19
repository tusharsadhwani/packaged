# packaged

The easiest way to ship python applications.

![Demo](https://raw.githubusercontent.com/tusharsadhwani/packaged/main/demo.jpg)

`packaged` can take any Python project, and package it into a self contained
executable, that can run on other machines without needing Python installed.

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

### Mandelbrot (`numpy`, `matplotlib`, GUI)

```bash
packaged ./mandelbrot.bin 'pip install -r requirements.txt' 'python mandelbrot.py' ./example/mandelbrot
```

This produces a `./mandelbrot.bin` binary with:

- Python 3.12
- `matplotlib`
- `numba`
- `llvmlite`
- `pillow`

That outputs an interactive mandelbrot set GUI.

### Minesweeper (using `packaged.toml` for configuration)

You can use a `packaged.toml` file and simply do `packaged path/to/project` to
create your package. For example, try the `minesweeper` project:

```bash
packaged ./example/minesweeper
```

[This configuration](https://github.com/tusharsadhwani/packaged/blob/main/example/minesweeper/packaged.toml)
is used for building the package. The equivalent command to build the project
without `pyproject.toml` would be:

```bash
packaged minesweeper.bin 'pip install .' 'python -m minesweeper' ./example/minesweeper
```

### Textual (TUI) Demo

Since the dependencies themselves contain all the source code needed, you can
skip the last argument. With this, no other files will be packaged other than
what is produced in the build step.

```bash
packaged ./textual.bin 'pip install textual' 'python -m textual'
```

This will simply package the `textual` library's own demo into a single file.

### Aliens (pygame)

Pygame ships with various games as well, `pygame.examples.aliens` is one of them:

```bash
packaged ./aliens 'pip install pygame' 'python -m pygame.examples.aliens'
```

Another one that you can try out is `pygame.examples.chimp`.

### IPython (console scripts)

Packages that expose shell scripts (like `ipython`) should also just work when
creating a package, and these scripts can be used as the startup command:

```bash
packaged ./ipython 'pip install ipython' 'ipython'
```

Now running `./ipython` runs a portable version of IPython!

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

## License

The package is Licensed under GNU General Public License v2 (GPLv2). However,
note that **the packages created with `packaged` are NOT licensed under GPL**.
This is because the archives created are just data for the package, and
`packaged` is not a part of the archives created.

That means that you can freely use `packaged` for commercial use.

Read the [License section for Makeself](https://github.com/megastep/makeself?tab=readme-ov-file#license) for more information.
