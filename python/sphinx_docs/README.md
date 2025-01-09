# Python scripts for building opm-simulators and opm-common sphinx documentation

## Installation of the python scripts
- Requires python3 >= 3.10

### Using poetry
For development it is recommended to use poetry:

- Install [poetry](https://python-poetry.org/docs/)
- Then run:
```
$ poetry install
$ poetry shell
```

### Installation into virtual environment
If you do not plan to change the code, you can do a regular installation into a VENV:

```
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install .
```

### Scripts

After installation, you can run the following scripts:

```
# Downloads docstrings JSON files and dune.module file before building the documentation locally
$ opmdoc-download-files
# Generate the documentation
$ make
# View the generated documentation in the browser
```
