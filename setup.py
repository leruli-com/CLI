#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = ["Click>=7.0", "requests", "tabulate", "minio", "docker", "tqdm>=4.62.0", "aiobotocore", "aiohttp"]

test_requirements = [
    "pytest>=3",
]

setup(
    author="leruli.com",
    author_email="info@leruli.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Use leruli.com from command line and Python code.",
    entry_points={
        "console_scripts": [
            "leruli=leruli.cli:main",
        ],
    },
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
    keywords="leruli",
    name="leruli",
    packages=find_packages(include=["leruli", "leruli.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    version="22.1.6",
    zip_safe=False,
)
