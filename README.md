# lib3mf (Python)

[![PyPI Version](https://img.shields.io/pypi/v/lib3mf)](https://pypi.org/project/lib3mf/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/lib3mf)](https://pypi.org/project/lib3mf/)
[![License](https://img.shields.io/pypi/l/lib3mf)](https://github.com/3MFConsortium/lib3mf/blob/main/LICENSE)
[![Build Status](https://github.com/3MFConsortium/lib3mf_python/actions/workflows/python-package.yml/badge.svg)](https://github.com/3MFConsortium/lib3mf_python/actions)
[![Python Versions](https://img.shields.io/pypi/pyversions/lib3mf)](https://pypi.org/project/lib3mf/)


This repository will holds the lib3mf python library to be published in PyPI.

## Preparing for release

After each release in lib3mf repository, one simply needs to run the `prepare_pypi_release.py` command as follows

```shell
python prepare_pypi_release 2.4.1a1
```

This command automatically updates all necessary artifacts based on the version number. 
Once completed, simply push the changes to Git.


## Manually building python wheels
To manually build the package, run:

```shell
python build_wheels.py
```

This script automatically detects the platform and builds the appropriate wheel.


## Automatic python wheel building and publishing

Every commit automatically builds and tests the python wheels for all 3 platforms.
Publishing to PyPI now happens only when a version tag is pushed (e.g. `v1.2.3`).
Push a tag after merging to trigger the publish step; regular commits and PRs continue
to build and test without deploying.
