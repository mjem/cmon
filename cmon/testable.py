#!/usr/bin/env python3

"""Implementation of Testable ABC."""

from typing import Iterable

class Testable:
	"""Base class for targets of a TestSuite."""
	def __init__(self,
				 label:str=None,
				 description:str=None,
				 important:bool=True):
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
		self.description = description
		self.important = important

	def links(self) -> Iterable["Testable"]:
		"""Return a list of objects that help provide the services of ourselves."""
		return []
