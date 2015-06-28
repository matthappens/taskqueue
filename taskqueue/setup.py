#!/usr/bin/env python

# TODO: Test this...

from setuptools import setup, find_packages

setup(
    name = "scarecrow-task-queue",
    version = "1.0",
    description = "A Flask server for accepting jobs and processing them in the cloud using AWS.",
    author = "Ben Holmes",
    author_email = "ben@bdholmes.com",
    url = "bdholmes.com",
    packages = find_packages(),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Flask",
    ],
    include_package_data = True,
    zip_safe = False,
    install_requires = ["flask", "gevent", "boto", "paramiko", "pycrypto", "Pillow", "ecdsa"]
)
