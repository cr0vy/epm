#!/usr/bin/env python3

import os
import sys
import setuptools
from setuptools import setup

setup(
    name="EPM",
    version="0.0.1",
    url="https://github.com/Cr0vy/epm",
    packages=setuptools.find_packages(),
    scripts=['bin/epm']
)

