#!/usr/bin/env python3

"""Implementation of terminal_dashboard() function."""

from .dashboard import Dashboard
from .terminalprinter import TerminalPrinter

def terminal_dashboard(dashboard:Dashboard,
					   output:TerminalPrinter,
					   results:dict):
	"""Show test results to terminal.

	Result is dict of test suite name against test suite results.
	Test suite results is dict of tuple of test, target against measurement.

	"""
	output.begin_section("Results for dashboard {dash}".format(dash=dashboard.label or "Dashboard"))
	for test_suite, test_suite_results in results.items():
		targets = set(r[1] for r in test_suite_results)
		# targets = {}
		# for (test, target), measurements in test_suite_results.items():
			# if target not in targets:
				# targets[target] = {}

			# if test not in targets[target]:
				# targets[target][test] = []

			# targets[target][test].append(measurements)

		if len(targets) == 0:
			continue

		output.begin_section("Test suite {suite}".format(
			suite="anon" if test_suite.label is None else test_suite.label))
		for target in targets:
			output.begin_section("{targettype} {label}".format(
				targettype=target.__class__.__name__,
				label=target.label or "anon"))
			# tests = set(r[0] for r in test_suite_results if r[1]
			for (test, test_target), measurement in test_suite_results.items():
				# print("test_target",test_target,"test",test,"measurements",measurements,"target",target)
				if test_target is not target:
					continue

				output.begin_section("{testname}".format(
					testname=getattr(test, "label", test.__name__)),
									 measurement.state.value)
				for message in measurement.messages:
					output.write_line("{label}: {value}".format(
						label=message.name, value=message.value))

				output.end_section()

			link_strs = []
			for link in target.links():
				link_strs.append(link.label or "anon")

			if len(link_strs) > 0:
				output.write_line("links: {links}".format(links=", ".join(link_strs)))

			output.end_section()

		output.end_section()
