#!/bin/bash -l

source scl_source enable rh-ruby26

python -m pip install . && \
python build.py

