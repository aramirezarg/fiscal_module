# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in fiscal_module/__init__.py
from fiscal_module import __version__ as version

setup(
	name='fiscal_module',
	version=version,
	description='Fiscal Module',
	author='CETI',
	author_email='info@ceti.systems',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
