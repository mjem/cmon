#!/usr/bin/env python3

"""Implementation of Dashboard class."""

import logging
from typing import Dict

from .testsuite import TestSuite
from .context import Context
from .measurement import Measurement
from .measurement import MeasurementState

logger = logging.getLogger()

class Dashboard:
	"""A group of related test suites."""
	def __init__(self,
				 test_suites:Dict[str, TestSuite],
				 nav_title:str=None,
				 nav_url:str=None,
				 nav_tooltip:str=None,
				 label:str=None):
		"""Args:
		- `nav_title`: Title text for first item in navigation bar
		- `nav_url`: Link for first item in navigation bar
		- `nav_tooltip`: Tooltip for first item in navigation bar
		- `test_suites`: List of test suites included in this dashboard
		- `label`: Title for this dashboard
		"""
		self.nav_title = nav_title
		self.nav_url = nav_url
		self.nav_tooltip = nav_tooltip
		self.test_suites = test_suites
		self.label = label

	def run(self, context:Context) -> Measurement:
		"""Run all tests to produce the dashboard result.

		Return heirarchy of Measurement objects, each containing
		- state
		- messages
		- children
		- subject (dashboard, testsuite,
		"""
		logger.info("Dashboard run")
		result = Measurement(subject=self)
		for suite in self.test_suites.values():
			suite_result = suite.run(context=context)
			if suite_result.state is MeasurementState.NOT_APPLICABLE:
				continue

			assert isinstance(suite_result.subject, TestSuite), type(suite_result.subject)
			result.add_child(suite_result)

		result.traffic_lights()
		return result

	def show(self,
			 target:object) -> None:
		"""Hierarchical console tree view of our configuration."""
		target.begin_section("Dashboard" + target.label(self.label))
		for k, v in self.test_suites.items():
			target.begin_section("Test suite" + target.label(name=k, label=v.label))
			v.show(target)
			target.end_section()

		target.end_section()
