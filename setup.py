#!/usr/bin/env python3

# pylint: skip-file
from setuptools import find_packages, setup

# read the contents of your README file and add it to the long_description
with open("readme.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="gen_openapi_rest",
    version="0.0.2",
    packages=find_packages(),
    description="Generate .http files from OpenAPI/Swagger JSON",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="rangulvers",
    url="https://github.com/rangulvers/openapi-rest-client-generator",
    license="LICENSE",
    install_requires=["requests"],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.org/classifiers/
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
