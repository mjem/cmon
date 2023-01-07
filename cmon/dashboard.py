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
		logger.info("Dashboard run")
		for suite in self.test_suites.values():
			suite.run(context=context)

	def show(self,
			 target:object) -> None:
		"""Hierarchical tree view of our configuration."""
		target.begin_section("Dashboard" + target.label(self.label))
		for k, v in self.test_suites.items():
			target.begin_section("Test suite" + target.label(name=k, label=v.label))
			v.show(target)
			target.end_section()

		target.end_section()
