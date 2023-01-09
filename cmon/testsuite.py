#!/usr/bin/env python3

import logging
from typing import Iterable
from typing import Callable

from .testable import Testable
from .context import Context
from .measurement import MeasurementState
from .measurement import Measurement

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
				printer.write_line("{name} ({label})".format(
					name=k, label=v.label))

			else:
				printer.write_line(k)

		printer.end_section()
		printer.begin_section("Tests")
		for t in self.tests:
			if hasattr(t, "label"):
				printer.write_line(t.label)

			else:
				printer.write_line(printer.docstring_single(t))

		printer.end_section()

	def run(self, context:Context) -> {}:
		"""Returns map of (test, target): measurement
		"""
		result = {}
		skip = len(self.targets) == 0 or len(self.tests) == 0
		logger.info("Testsuite {label} with {cctargets} targets {cctests} tests {action}".format(
			label="anon" if self.label is None else self.label,
			cctargets=len(self.targets),
			cctests=len(self.tests),
			action="skip" if skip else "run"))

		if skip:
			return result

		for target_name, target in self.targets.items():
			logger.info("Target {target}".format(target=target_name))
			for test in self.tests:
				measurement = test(target=target, context=context)
				assert isinstance(measurement, Measurement), \
					"Bad result {r} from {t}".format(r=measurement, t=test)
				if measurement.state is MeasurementState.NOT_APPLICABLE:
					continue

				logger.info("Test {test} returns {result} with {msgs} additional messages".format(
					test=getattr(test, "label", test.__name__),
					result=measurement,
					msgs=len(measurement.messages)))

				result[(test, target)] = measurement

		return result
