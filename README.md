lib3mf (Python)
=========

This repository will holds the lib3mf python library to be published in PyPI.
After each release in lib3mf repository, one simply needs to run the `prepare_pypi_release.py` command as follows

```shell
python prepare_pypi_release 2.3.2
```

This command automatically updates all necessary artifacts based on the version number. 
Once completed, simply push the changes to Git.

To manually build the package, run:

```shell
python build_wheels.py
```

This script automatically detects the platform and builds the appropriate wheel.