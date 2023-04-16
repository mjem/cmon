#!/usr/bin/env python3

"""Command line UI."""

# PYTHON_ARGCOMPLETE_OK enable argcomplete global completion

import logging
import argparse
import runpy
from pathlib import Path

import dotenv
import argcomplete

from .context import Context
from .htmldashboard import html_dashboards
from .log import init_log
from .terminaldashboard import terminal_dashboards
from .terminalprinter import TerminalPrinter
from .result import result_lines


def main():
	"""Command line entry point."""
	parser = argparse.ArgumentParser(
		description="Runtime tests of a system of servers",
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("--show-config",
						action="store_true",
						help="Show dashboard configuration to console")
	parser.add_argument("--show-subjects",
						action="store_true",
						help="List all testable subjects, not sorted into dashboards")
	# parser.add_argument("--simulate",
						# action="store_true",
						# help=("Pretend to execute all measurements in the dashboard, "
							  # "logging actions and validating configuration"))
	parser.add_argument("--output-terminal",
						action="store_true",
						help="Run test suites and show output as text to console")
	parser.add_argument("--output-html",
						metavar="FILE",
						# type=argparse.FileType('w'),
						help="Run test suites and show output as a webpage")
	# parser.add_argument("--output-yaml",
	# metavar="FILE",
	# help="Run test suites and show output in YAML format")
	# parser.add_argument("--show-config-yaml",
	# action="store_true",
	# help="Output YAML-formatted version of config file")
	# parser.add_argument("--output-system-design",
						# action="store_true",
						# help="Output PlantUML formatted system design diagram")
	parser.add_argument("--output-result",
						action="store_true",
						help="Just list outputs in a database friendly way")
	parser.add_argument("--verbose",
						action="store_true",
						help="More verbose output")
	parser.add_argument("--config-py",
						help="Load configuration from python file")
	# parser.add_argument("--config-yaml",
	# help="Load configuration from YAML file")
	# parser.add_argument("--exclude-tests",
	# help="List named tests to exclude")
	parser.add_argument("--include-tests",
						nargs="+",
						help="Only run named tests")
	parser.add_argument("--include-subjects",
						nargs="+",
						help="Only run named subjects")
	parser.add_argument("--logtest",
						action="store_true",
						help="To a quick test of logging system and quit")
	argcomplete.autocomplete(parser)
	args = parser.parse_args()

	# read basic dotenv configuration file
	config = dotenv.dotenv_values(".env")
	if "CONFIG_PY" in config:
		args.config_py = config["CONFIG_PY"]

	init_log(level=logging.DEBUG if args.verbose else logging.WARNING)

	if args.logtest:
		logger = logging.getLogger()
		logger.debug("an debug")
		logger.info("an info")
		logger.warning("an warning")
		logger.error("an error")
		logger.critical("an critical")
		parser.exit()

	config = None
	if args.config_py:
		config = runpy.run_path(args.config_py)

	if config is None:
		parser.error("No configuration file given")

	system = config.get("system")
	if system is None:
		parser.error("Config file is missing system object")

	if args.show_config:
		target = TerminalPrinter()
		for dashboard in system.dashboards.values():
			dashboard.show(target)

		parser.exit()

	# if args.output_system_design:
		# raise NotImplementedError()

	if args.show_subjects:
		target = TerminalPrinter()
		for subject in system.all_subjects():
			target.write_line("{type} {label}".format(
				type=type(subject).__name__, label=subject.label))

		parser.exit()

	all_results = system.run(Context(simulate=False,
									 verbose=args.verbose,
									 include_tests=args.include_tests,
									 include_subjects=args.include_subjects))

	if args.output_result:
		for subject_results in all_results.values():
			for result in subject_results:
				result_lines(TerminalPrinter(), result)

		parser.exit()

	if args.output_terminal:
		terminal_dashboards(TerminalPrinter(), system, all_results)
		parser.exit()

	if args.output_html:
		html_dashboards(output_dir=Path(args.output_html),
						system=system,
						results=all_results,
						config_file=Path(args.config_py))
		parser.exit()

	parser.error("No actions specified")
