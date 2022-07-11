#!/usr/bin/env python


from pathlib import Path
import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setuptools.setup(
    name="grouper",
    version="1.0",
    author="Lars Skodje",
    author_email="larsskod@gmail.com",
    description="Python regular expression grouper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["grouper"],
)
