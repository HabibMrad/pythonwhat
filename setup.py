#!/usr/bin/env python

from distutils.core import setup

setup(
	name='pythonwhat',
	version='2.6.0',
	packages=['pythonwhat', 'pythonwhat.test_funcs'],
	install_requires=["dill", "IPython", "numpy", "pandas", "markdown2", "jinja2"]
)
