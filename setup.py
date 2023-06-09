#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from setuptools import setup, find_packages

MAJOR = 0
MINOR = 0
PATCH = 5
VERSION = f"{MAJOR}.{MINOR}.{PATCH}"

setup(
    name="sonic-uia2-client",
    version=VERSION,
    author="SonicCloudOrg",
    author_email="soniccloudorg@163.com",
    long_description_content_type="text/markdown",
    url='https://github.com/SonicCloudOrg/sonic-uiautomator2-python-client',
    long_description=open('README.md', encoding="utf-8").read(),
    python_requires=">=3",
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing'
    ],
)
