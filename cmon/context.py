#!/usr/bin/env python

"""Implementation of Context object."""

from typing import Iterable
from datetime import datetime

class Context:
	"""Runtime state passed to every test function."""
	def __init__(self,
				 simulate:bool=False,
				 verbose:bool=False,
				 include_tests:Iterable[str]=None,
				 include_subjects:Iterable[str]=None):
		self.simulate = simulate
		self.verbose = verbose
		self.include_tests = include_tests
		self.include_subjects = include_subjects
		self.execute_start = datetime.utcnow()
