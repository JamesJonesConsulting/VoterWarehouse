#!/bin/sh -l

BINARY_BASENAME=$1
VERSION=$2

/usr/bin/python -m pip install .
/usr/bin/python build.py
