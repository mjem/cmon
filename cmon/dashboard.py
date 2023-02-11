#!/usr/bin/env python3

"""Implementation of Dashboard class."""

import logging
from typing import Dict
from typing import Iterable
from datetime import datetime

from .testsuite import TestSuite
from .context import Context
from .measurement import Measurement
from .measurement import MeasurementState
from .testable import Testable

logger = logging.getLogger()

class Dashboard:
	"""A group of related test suites."""
	def __init__(self,
				 test_suites:Dict[str, TestSuite],
				 label:str=None,
				 description:str=None):
		"""Args:
		- `test_suites`: List of test suites included in this dashboard
		- `label`: Title for this dashboard
		"""
		self.test_suites = test_suites
		self.label = label
		self.description = description

	def run(self,
			standard_tests:dict[Testable,Iterable[Measurement]],
			context:Context) -> Measurement:
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
			suite_result = suite.run(standard_tests=standard_tests, context=context)
			if suite_result.state is MeasurementState.NOT_APPLICABLE:
				continue

			assert isinstance(suite_result.subject, TestSuite), type(suite_result.subject)
			result.add_child(suite_result)

		result.traffic_lights()
		result.add_message("Execute start", context.execute_start)
		result.add_message("Execute stop", datetime.utcnow())
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
