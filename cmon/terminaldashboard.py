#!/usr/bin/env python3

"""Implementation of terminal_dashboard() function."""

from .dashboard import Dashboard
from .terminalprinter import TerminalPrinter
from .measurement import Measurement

def terminal_dashboard(output:TerminalPrinter,
					   dashboard_results:Measurement):
	"""Show test results to terminal.

	Result is dict of test suite name against test suite results.
	Test suite results is dict of tuple of test, target against measurement.

	"""
	dashboard = dashboard_results.subject
	output.begin_section("Results for dashboard {dash}".format(dash=dashboard.label or "Dashboard"))
	for test_suite_results in dashboard_results.children:
		test_suite = test_suite_results.subject
		output.begin_section("Test suite {suite}".format(
			suite="anon" if test_suite.label is None else test_suite.label))
		for target_results in test_suite_results.children:
			target = target_results.subject
			output.begin_section("{targettype} {label}".format(
				targettype=target.__class__.__name__,
				label=target.label or "anon"))
			for test_result in target_results.children:
				test = test_result.subject
				output.begin_section("{testname}".format(
					testname=getattr(test, "label", test.__name__)),
									 test_result.state.value)
				for message in test_result.messages:
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
