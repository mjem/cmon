#!/usr/bin/env python3

"""Implementation of Testable ABC."""

from typing import Iterable

class Testable:
	"""Base class for targets of a TestSuite."""
	# name class attribute is written to the results file
	name = "testable (base)"
	# label class attribute is used as the main visible label in the web output
	label = "Testable (base)"
	# full description may be shown in a tooltip in the website
	description = "This is a base class and should not be instantiated"

	def __init__(self,
				 label:str,
				 name:str=None,
				 description:str=None,
				 important:bool=True,
				 tests:Iterable["Measurement"]=None):
		"""Args:
		- `label`: Short friendly label to display in dashboard
		  (item names are internal and not shown in outputs)
		- `description`: Long description (for tooltip) of subject
		- `important`: If an important item fails a test, then the item is shown
		  as failed and all parent items as shown as mixed or failed.
		  But if the item is not `important` it's not counted in the traffic light
		  computation of parent items, which can still pass
		"""
		self.label = label
		self.name = name
		self.description = description
		self.important = important
		self.tests = tests

	def links(self) -> Iterable["Testable"]:
		"""Return a list of objects that help provide the services of ourselves."""
		return []

	def get_id(self) -> str:
		"""Return a reasonably unique identifier. For storing results in database."""
		return self.name or self.label

	def __str__(self) -> str:
		return "Subject {c} ({n})".format(c=type(self).__name__, n=self.name)
