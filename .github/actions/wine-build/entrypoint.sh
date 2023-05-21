#!/bin/sh -l

BINARY_BASENAME=$1
VERSION=$2

/usr/bin/python -m pip install .
/usr/bin/python build.py
if [[ "$GITHUB_REF" =~ ^refs/tags.* ]]; then
  VERSION=$GITHUB_REF_NAME
else
  VERSION=$(echo "${GITHUB_REF_NAME}" | sed 's|/|-|g')
fi
cd dist
zip -rm "${BINARY_BASENAME}-${VERSION}-windows-x86_64.zip" "${BINARY_BASENAME}.exe"
