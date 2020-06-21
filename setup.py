#!/usr/bin/env python

"""
London: Data Importer
"""

from setuptools import setup, find_packages

setup(
    name='london',
    version='0.0.1',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/cohoe/london',
    license='LICENSE.txt',
    author='Grant Cohoe',
    author_email='grant@grantcohoe.com',
    description='A cocktail recipe management system',
    long_description=__doc__,
    scripts=['scripts/london'],
    install_requires=[
        'barbados',
        'python-editor',
        'PyYAML',
        'jinja2',
        'ruamel.yaml'
    ]
)
