#!/usr/bin/env python

"""Implementation of Context object."""

from datetime import datetime

class Context:
	"""Runtime state passed to every test function."""
	def __init__(self,
				 simulate:bool=False,
				 verbose:bool=False,
				 include_tests=None,
				 # exclude_tests,
				 ):
		self.simulate = simulate
		self.verbose = verbose
		self.include_tests = include_tests
		self.execute_start = datetime.utcnow()
