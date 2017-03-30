# vagrepo

[![Build Status](https://travis-ci.org/matthijsbos/vagrepo.svg?branch=master)](https://travis-ci.org/matthijsbos/vagrepo)

Local vagrant box repository manager

## Proposed interface
```
vagrepo list
vagrepo create BOX_NAME [--description BOX_DESCRIPTION]
vagrepo edit BOX_NAME [--name NEW_NAME] [--description NEW_DESCRIPTION]
vagrepo add BOX_NAME BOX_FILE_PATH
vagrepo remove BOX_NAME BOX_VERSION
vagrepo metadata BOX_NAME
```

