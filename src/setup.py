#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      
      name='tsimsar',
      version='0.0.4',
      url="https://github.com/lucienne1986/Python-Projects",
      author="Lucienne Micallef",
      author_email="lucienne1986@gmail.com",
      description='Testing installation of Package SIMSAR',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      #install_requires=[
      #'git', 'os', 're', 'Template', 'pycurl', 'wget', 'subprocess', 'pathlib',
      #'textwarp', 'glob', 'netCDF4', 'configparser'],
      py_modules=["tsimsar"],
      packages=setuptools.find_packages(),
      #package_dir={'':'tsimsar'},
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
      python_requires=">=3.6",     
      )
