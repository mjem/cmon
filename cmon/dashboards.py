#!/usr/bin/env python3

"""Implementation of the Flock class."""

import logging
from typing import Iterable

from .dashboard import Dashboard
from .context import Context
from .measurement import Measurement
from .testable import Testable

logger = logging.getLogger("dashboards")

class Dashboards:
	"""A group of dashboards."""
	def __init__(self,
				 dashboards:Iterable[Dashboard],
				 standard_tests:dict[Testable,Iterable[Measurement]]={},
				 nav_title:str=None,
				 nav_url:str=None,
				 nav_tooltip:str=None):
		"""Args:
		- `nav_title`: Title text for first item in navigation bar
		- `nav_url`: Link for first item in navigation bar
		- `nav_tooltip`: Tooltip for first item in navigation bar
		"""
		self.dashboards = dashboards
		self.standard_tests = standard_tests
		self.nav_title = nav_title
		self.nav_url = nav_url
		self.nav_tooltip = nav_tooltip

	def run(self, context:Context):
		logger.info("Bundle of dashboards run")
		result = Measurement(subject=self)
		for dashboard in self.dashboards.values():
			result.add_child(dashboard.run(standard_tests=self.standard_tests, context=context))

		return result
