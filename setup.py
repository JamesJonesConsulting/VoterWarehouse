# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages
from Warehouse.version import __version__

with open('README.rst', encoding='UTF-8') as f:
    readme = f.read()

with open('LICENSE', encoding='UTF-8') as f:
    license_content = f.read()

setup(
    name='voterwarehouse',
    version=__version__,
    description='Imports Voter and Voter Histories into a data warehouse',
    long_description=readme,
    author='James Jones',
    author_email='jamjon3@gmail.com',
    url='https://github.com/JamesJonesConsulting/VoterWarehouse',
    license=license_content,
    packages=find_packages(exclude=('tests', 'docs')),
    python_requires=">=3.11",
    scripts=['voterwarehouse.py'],
    install_requires=[
        "PyMySQL==1.0.3",
        "PyYAML==6.0",
        "sphinx==5.3.0",
        "nose==1.3.7",
        "pyinstaller==5.11.0"
    ]
)
