#!/usr/bin/env python3

import logging
from typing import Iterable
from typing import Callable
from typing import Dict

from .testable import Testable
from .measurement import MeasurementState
from .measurement import Measurement
from .context import Context

logger = logging.getLogger("testsuite")

class TestSuite:
	def __init__(self,
				 subjects:Dict[str, Testable],
				 label:str,
				 description:str=None):
		self.subjects = subjects
		self.label = label
		self.description = description

		# set name attribute of each subject to the key
		for k, v in subjects.items():
			if v.name is None:
				v.name = k

	def show(self, printer:object) -> None:
		"""Hierarchical tree view of our configuration."""
		printer.begin_section("Subjects")
		for k, v in self.subjects.items():
			if v.label is not None:
				title = "{name} ({label})".format(
					name=k, label=v.label)

			else:
				title = k

			if len(v.links()) == 0:
				printer.write_line(title)

			else:
				printer.begin_section(title)
				for l in v.links():
					printer.write_line(str(l))

				printer.end_section()

		printer.end_section()

	def run(self,
			standard_tests:dict[Testable,Iterable[Measurement]],
			context:Context) -> Measurement:
		"""Run all tests in the suite."""
		logger.info("Testsuite {label} with {cctargets} targets".format(
			label="anon" if self.label is None else self.label,
			cctargets=len(self.targets)))

		if len(self.targets) == 0:
			# if we have no tests configred or no targets then we cannot run
			return Measurement(MeasurementState.NOT_APPLICABLE)

		suite_result = Measurement(subject=self)
		for target_name, target in self.targets.items():
			logger.info("Target {target}".format(target=target_name))
			target_result = Measurement(subject=target)
			if target.tests is not None:
				tests = target.tests

			else:
				tests = standard_tests.get(type(target))

			if tests is None or len(tests) == 0:
				logger.info("Skipping subject with no tests")
				return Measurement(MeasurementState.NOT_APPLICABLE)

			for test in tests:
				# check if the user has excluded any tests
				if hasattr(test, "label") and\
				   context.include_tests is not None and\
				   context.include_tests not in test.label:
					continue

				test_result = test(target=target, context=context)
				assert isinstance(test_result, Measurement), \
					"Bad result {r} from {t}".format(r=test_result, t=test)
				if test_result.state is MeasurementState.NOT_APPLICABLE:
					continue

				logger.info("Test {test} returns {result} with {msgs} additional messages".format(
					test=getattr(test, "label", test.__name__),
					result=test_result,
					msgs=len(test_result.messages)))

				test_result.subject = test
				target_result.add_child(test_result)

			target_result.traffic_lights()
			if len(target_result.children) > 0:
				suite_result.add_child(target_result)

		suite_result.traffic_lights()
		assert isinstance(suite_result.subject, TestSuite), type(suite_result)
		return suite_result
