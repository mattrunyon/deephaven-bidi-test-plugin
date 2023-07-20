# Deephaven Bidi Test Plugin

## Build

To create your build / development environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools build
```

To build:

```sh
python -m build --wheel
```

produces the wheel into `dist/`.
