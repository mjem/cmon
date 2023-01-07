#!/usr/bin/env python

"""Implementation of Context object."""

class Context:
	"""Runtime state passed to every test function."""
	def __init__(self,
				 simulate:bool=False,
				 verbose:bool=False,
				 # exclude_tests,
				 # include_tests,
				 ):
		self.simulate = simulate
		self.verbose = verbose
