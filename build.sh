#!/usr/bin/env bash

python -m venv venv
source venv/bin/activate

python -m pip install -r requirements.txt

python build.py

docker build --no-cache \
  --build-arg VERSION=1.0.0 \
  --build-arg ITERATION=1 \
  -v "$(pwd)/dist:/dist:Z" .