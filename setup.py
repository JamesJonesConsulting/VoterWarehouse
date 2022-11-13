# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license_content = f.read()

setup(
    name='sample',
    version='3.0.0',
    description='Sample package for Python-Guide.org',
    long_description=readme,
    author='James Jones',
    author_email='jamjon3@gmail.com',
    url='https://github.com/kennethreitz/samplemod',
    license=license_content,
    packages=find_packages(exclude=('tests', 'docs'))
)