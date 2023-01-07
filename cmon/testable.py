#!/usr/bin/env python3

"""Implementation of Testable ABC."""

class Testable:
	"""Base class for targets of a TestSuite."""
	def __init__(self, label=None):
		self.label = label
