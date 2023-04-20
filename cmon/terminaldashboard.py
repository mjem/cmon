#!/usr/bin/env python3

"""Implementation of terminal_dashboard() function."""

from typing import Dict
from typing import Iterable
from collections import defaultdict

from .dashboard import Dashboard
from .terminalprinter import TerminalPrinter
from .measurement import Measurement
from .measurement import MeasurementState
from .measurement import traffic_light
from .testable import Testable
from .system import System

def terminal_dashboards(output:TerminalPrinter,
						# dashboards:Dict[str, Dashboard],
						system: System,
						results:Dict[Testable, Iterable[Measurement]]) -> None:
	"""Show test results to terminal.
	"""
	# print("terminal dashboards output", output, "dashboards", dashboards, "results", results)
	# prescan and build dict subject:result
	# map of subject to result
	# subject_results = defaultdict(list)
	# for result in results:
		# subject_results[result.subject].append(result)

	dashboards = system.dashboards

	# Count how many child nodes each object has with test results,
	# so we can easily prune empty nodes below
	# Traffic light status for container objects
	children = {}
	trafficlight = {}
	for dashboard in dashboards.values():
		trafficlight[dashboard] = MeasurementState.EMPTY
		children[dashboard] = 0
		for test_suite in dashboard.test_suites.values():
			trafficlight[test_suite] = MeasurementState.EMPTY
			children[test_suite] = 0
			for subject in test_suite.subjects.values():
				trafficlight[subject] = MeasurementState.EMPTY
				children[dashboard] += len(results[subject])
				children[test_suite] += len(results[subject])
				children[subject] = len(results[subject])
				for measurement in results[subject]:
					traffic_light(trafficlight, dashboard, measurement.state)
					traffic_light(trafficlight, test_suite, measurement.state)
					traffic_light(trafficlight, subject, measurement.state)

	for dashboard in dashboards.values():
		if children[dashboard] == 0:
			continue

		output.begin_section(
			section="Dashboard {dash}".format(dash=dashboard.label),
			postfix=trafficlight[dashboard].value)
		for test_suite in dashboard.test_suites.values():
			if children[test_suite] == 0:
				continue

			output.begin_section(
				section="Testsuite {suite}".format(suite=test_suite.label),
				postfix=trafficlight[test_suite].value)
			for subject in test_suite.subjects.values():
				if children[subject] == 0:
					continue

				output.begin_section(
					section="{targettype} {label}".format(
						targettype=subject.__class__.__name__,
						label=subject.label),
					postfix=trafficlight[subject].value)
				for result in results[subject]:
					if result.state is MeasurementState.NOT_APPLICABLE:
						continue

					output.begin_section("Test {testname}".format(
						testname=result.test_fn.label),
										 result.state.value)
					for line in result.message_lines():
						output.write_line(line)

					output.end_section()

				# link_strs = []
				# for link in target.links():
					# link_strs.append(link.label or "anon")

				# if len(link_strs) > 0:
					# output.write_line("Links: {links}".format(links=", ".join(link_strs)))

				output.end_section()

			output.end_section()

		output.end_section()

