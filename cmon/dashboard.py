#!/usr/bin/env python3

"""Implementation of Dashboard class."""

import logging
from typing import Dict

from .testsuite import TestSuite
from .context import Context

logger = logging.getLogger()

class Dashboard:
	def __init__(self,
				 test_suites:Dict[str, TestSuite],
				 label:str=None):
		self.test_suites = test_suites
		self.label = label

	def run(self, context:Context) -> {}:
		"""
		Return heirarchy of Measurement objects, each containing
		- state
		- messages
		- children
		- subject (dashboard, testsuite,

		Return map of tuples of (testsuite, test, target): measurement

		Return map of testsuite: (test, target): measurement
		"""
		logger.info("Dashboard run")
		result = {}
		for suite in self.test_suites.values():
			result[suite] = suite.run(context=context)

		return result

	def show(self,
			 target:object) -> None:
		"""Hierarchical tree view of our configuration."""
		target.begin_section("Dashboard" + target.label(self.label))
		for k, v in self.test_suites.items():
			target.begin_section("Test suite" + target.label(name=k, label=v.label))
			v.show(target)
			target.end_section()

		target.end_section()
