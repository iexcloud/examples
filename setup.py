# *****************************************************************************
#
# Copyright (c) 2021, the iexexamples authors.
#
# This file is part of the iexexamples library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#

import io
import os
import os.path
from codecs import open

from setuptools import find_packages, setup

pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))
name = "iexexamples"


def get_version(file, name="__version__"):
    path = os.path.realpath(file)
    version_ns = {}
    with io.open(path, encoding="utf8") as f:
        exec(f.read(), {}, version_ns)
    return version_ns[name]


version = get_version(pjoin(here, name, "_version.py"))

with open(pjoin(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read().replace("\r\n", "\n")

requires = [
    "dash>=1.20.0",
    "dash-core-components>=1.16.0",
    "dash-html-components>=1.1.3",
    "dash-renderer>=1.9.1",
    "plotly>=5.0.0",
    "pandas>=1.",
    "pyEX @ git+https://git@github.com/iexcloud/pyEX@main#egg=pyEX",
]

requires_dev = requires + [
    "black>=20.",
    "bump2version>=1.0.0",
    "flake8>=3.7.8",
    "flake8-black>=0.2.1",
    "mock",
    "pytest>=4.3.0",
    "pytest-cov>=2.6.1",
    "recommonmark",
    "Sphinx>=1.8.4",
    "sphinx-markdown-builder>=0.5.2",
    "sphinx-rtd-theme",
]

setup(
    name=name,
    version=version,
    description="IEX Example Apps and Utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iexcloud/{name}".format(name=name),
    author="IEX Cloud",
    author_email="dev@iexcloud.io",
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="finance data",
    zip_safe=False,
    packages=find_packages(exclude=[]),
    install_requires=requires,
    extras_require={
        "dev": requires_dev,
    },
)
