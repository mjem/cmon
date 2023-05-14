#!/usr/bin/env python3

"""Implementation of the System class."""

import logging
from typing import Iterable
from typing import Dict
from collections import defaultdict
from fnmatch import fnmatch

from .dashboard import Dashboard
from .context import Context
from .measurement import Measurement
from .measurement import measure
from .testable import Testable
from .testable import Testable

logger = logging.getLogger("dashboards")

class Navigation:
	"""Information about a link."""
	def __init__(self,
				 title:str,
				 url:str,
				 tooltip:str=None):
		self.title = title
		self.url = url
		self.tooltip = tooltip

class System:
	"""Representation of a complete test environment."""
	def __init__(self,
				 navigation:Navigation=None,
				 standard_tests:dict[Testable,Iterable[Measurement]]={},
				 dashboards:dict[str, Iterable[Dashboard]]={}):
		"""Args:
		- `nav_title`: Title text for first item in navigation bar
		- `nav_url`: Link for first item in navigation bar
		- `nav_tooltip`: Tooltip for first item in navigation bar
		"""
		self.navigation = navigation
		self.standard_tests = standard_tests
		self.dashboards = dashboards

	def all_subjects(self) -> Iterable[Testable]:
		"""Return flattened list of all subjects."""
		subjects = []
		for dashboard in self.dashboards.values():
			for testsuite in dashboard.test_suites.values():
				subjects.extend(testsuite.subjects.values())

		return subjects

	def run(self, context:Context) -> Dict[Testable, Iterable[Measurement]]:
		"""Run all tests against all subjects and return a flat list of results."""
		results = defaultdict(list)  # Subject : list(Measurement)
		for subject in self.all_subjects():
			if context.include_subjects is not None:
				# print("test if subject excluded")
				include = False
				for include_subject in context.include_subjects:
					# print("testr if clause", include_subject, "includes it")
					if fnmatch(subject.name.lower(), include_subject.lower()):
						# print("included by", include_subject)
						include = True
						break

				if not include:
					# logger.info("  excluded")
					continue

			logger.info("Subject {s}".format(s=subject.name))

			# check if this subject has a unique list of tests defined in the config file
			if subject.tests:
				tests = subject.tests

			# otherwise use the normal tests for this subject type
			else:
				tests = self.standard_tests[type(subject)]

			for test in tests:
				if getattr(test, "decorator", None) is not measure:
					raise ValueError("Subject {s} has invalid test {t}".format(
						s=subject, t=test))

				logger.info("Test {t}".format(t=test.name))
				measurement = test(subject=subject, context=context)
				measurement.subject = subject
				measurement.test_fn = test
				for message in measurement.messages:
					# print("binding message name", message.name, "value", message.value)
					for message_description in test.messages:
						# print(" against message description", message_description.name)
						if message_description.name == message.name:
							message.description = message_description

				results[subject].append(measurement)
				logger.debug("Result {r}".format(r=measurement))

		return results
