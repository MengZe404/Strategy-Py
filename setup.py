#!/usr/bin/python3
from setuptools import setup, find_packages
setup(
	name = "Strategy-Py",
	version = "0.2",
	packages = find_packages(),
	scripts = ["strategy.py"],
	include_package_data = True,
	url="http://github.com/openMengZe/Strategy-Py",
	maintainer="MengZe",
	maintainer_email="hongmengze110@gmail.com"
)
