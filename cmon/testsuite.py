#!/usr/bin/env python3

import logging
from typing import Iterable
from typing import Callable

from .testable import Testable
from .measurement import MeasurementState
from .measurement import Measurement
from .context import Context

logger = logging.getLogger("testsuite")

class TestSuite:
	def __init__(self,
				 targets:Iterable[Testable],
				 tests:Iterable[callable],
				 label:str=None):
		self.targets = targets
		self.tests = tests
		self.label = label

	def show(self, printer:object) -> None:
		"""Hierarchical tree view of our configuration."""
		printer.begin_section("Targets")
		for k, v in self.targets.items():
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
		printer.begin_section("Tests")
		for t in self.tests:
			if hasattr(t, "label"):
				printer.write_line(t.label)

			else:
				printer.write_line(printer.docstring_single(t))

		printer.end_section()

	def run(self, context:Context) -> Measurement:
		"""
		"""
		skip = len(self.targets) == 0 or len(self.tests) == 0
		logger.info("Testsuite {label} with {cctargets} targets {cctests} tests {action}".format(
			label="anon" if self.label is None else self.label,
			cctargets=len(self.targets),
			cctests=len(self.tests),
			action="skip" if skip else "run"))

		if skip:
			# if we have no tests configred or no targets then we cannot run
			return Measurement(MeasurementState.NOT_APPLICABLE)

		suite_result = Measurement(subject=self)
		for target_name, target in self.targets.items():
			logger.info("Target {target}".format(target=target_name))
			target_result = Measurement(subject=target)
			for test in self.tests:
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
