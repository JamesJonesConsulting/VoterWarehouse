#!/usr/bin/env bash

rm -Rf venv
rm -f dist/*.{rpm,deb}

python -m venv venv
source venv/bin/activate

python -m pip install -r requirements.txt

python build.py

# Branch detection
GITREF=$(git symbolic-ref HEAD)

if [[ "$GITREF" =~ ^refs/tags.* ]]; then
  VERSION=$(git symbolic-ref --short HEAD)
else
  VERSION=$(dist/voterwarehouse -v)
  VERSION+="~"
  VERSION+=$(git symbolic-ref --short HEAD | sed 's|/|-|g')
fi

docker build --no-cache \
  --build-arg ITERATION=1 \
  --build-arg VERSION=${VERSION} \
  -v "$(pwd)/dist:/dist:Z" .