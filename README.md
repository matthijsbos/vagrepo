# vagrepo

[![Travis](https://img.shields.io/travis/matthijsbos/vagrepo.svg)](https://travis-ci.org/matthijsbos/vagrepo)[![PyPI](https://img.shields.io/pypi/pyversions/vagrepo.svg)](https://pypi.python.org/pypi/vagrepo)

Local vagrant box repository manager.

## Installation
`pip install vagrepo`

## Proposed interface
```
vagrepo list
vagrepo create BOX_NAME [--description BOX_DESCRIPTION]
vagrepo edit BOX_NAME [--name NEW_NAME] [--description NEW_DESCRIPTION]
vagrepo add BOX_NAME BOX_FILE_PATH
vagrepo remove BOX_NAME BOX_VERSION
vagrepo metadata BOX_NAME
```

