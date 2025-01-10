import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="utils",
    version="0.1",
    description="Utilities such as dataclasses and logger for amplec",
    long_description=long_description,
    install_requires=[
        'requests'
    ],
    long_description_content_type="text/markdown",
    url="https://github.com/amplec/utils",
    packages=["amplec_utils"])