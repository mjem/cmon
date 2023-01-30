#!/usr/bin/env python3

import argparse
import runpy
from pathlib import Path

from .log import init_log
from .terminalprinter import TerminalPrinter
from .terminaldashboard import terminal_dashboards
from .htmldashboard import html_dashboards
from .context import Context

def main():
	init_log()
	parser = argparse.ArgumentParser()
	parser.add_argument("--show-config",
						action="store_true",
						help="Show current configuration to console")
	parser.add_argument("--simulate",
						action="store_true",
						help=("Pretend to execute all measurements in the dashboard, "
							  "logging actions and validating configuration"))
	parser.add_argument("--output-console",
						action="store_true",
						help="Run test suites and show output as text to console")
	parser.add_argument("--output-web",
						metavar="FILE",
						help="Run test suites and show output as a webpage")
	# parser.add_argument("--output-yaml",
						# metavar="FILE",
						# help="Run test suites and show output in YAML format")
	# parser.add_argument("--show-config-yaml",
						# action="store_true",
						# help="Output YAML-formatted version of config file")
	parser.add_argument("--output-system-design",
						action="store_true",
						help="Output PlantUML formatted system design diagram")
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
						help="Only run named tests")
	args = parser.parse_args()
	# from . import config

	config = None
	dashboard = None
	if args.config_py:
		config = runpy.run_path(args.config_py)#, init_globals=globals()))
		dashboards = config["dashboards"]

	if config is None:
		parser.error("No configuration file given")

	if args.show_config:
		for dashboard in dashboards.dashboards.values():
			dashboard.show(TerminalPrinter())
			parser.exit()

	# if args.show_config_yaml:
		# raise NotImplementedError()

	if args.output_system_design:
		raise NotImplementedError()

	# if args.config_yaml:
		# raise NotImplementedError()

	if args.output_console or args.output_web:
		result = dashboards.run(Context(simulate=args.simulate,
										verbose=args.verbose,
										include_tests=args.include_tests))

		if args.simulate:
			parser.exit()

		if args.output_console:
			terminal_dashboards(TerminalPrinter(), result)

		if args.output_web:
			html_dashboards(result, Path(args.output_web), Path(args.config_py))

		parser.exit()

	parser.error("No actions specified")
