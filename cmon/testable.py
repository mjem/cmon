#!/usr/bin/env python3

"""Implementation of Testable ABC."""

from typing import Iterable

class Testable:
	"""Base class for targets of a TestSuite."""
	def __init__(self, label=None):
		self.label = label

	def links(self) -> Iterable["Testable"]:
		"""Return a list of objects that help provide the services of ourselves."""
		return []
