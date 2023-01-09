#!/usr/bin/env python3

import argparse
import runpy
from pathlib import Path

from .log import init_log
from .terminalprinter import TerminalPrinter
from .terminaldashboard import terminal_dashboard
from .htmldashboard import html_dashboard
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
	parser.add_argument("--output-html",
						metavar="FILE",
						help="Run test suites and show output as a webpage")
	parser.add_argument("--verbose",
						action="store_true",
						help="More verbose output")
	parser.add_argument("--config-py",
						help="Load configuration from python file")
	# parser.add_argument("--exclude-tests",
						# help="List named tests to exclude")
	# parser.add_argument("--include-tests",
						# help="Only run named tests")
	# --test-dirs allow extra local python tests
	# parser.add_argument("--exclude-servers")
	# parser.add_argument("--include-servers")
	# parser.add_argument("--exclude-suites")
	# parser.add_argument("--include-suites")
	args = parser.parse_args()
	# from . import config

	config = None
	dashboard = None
	if args.config_py:
		config = runpy.run_path(args.config_py)#, init_globals=globals()))
		dashboard = config["dashboard"]

	if config is None:
		parser.error("No configuration file given")

	if args.show_config:
		dashboard.show(TerminalPrinter())
		parser.exit()

	context=Context(simulate=args.simulate,
					verbose=args.verbose)

	if args.output_console or args.output_html:
		result = dashboard.run(context)

		if args.simulate:
			parser.exit()

		if args.output_console:
			terminal_dashboard(dashboard, TerminalPrinter(), result)

		if args.output_html:
			html_dashboard(dashboard, result, Path(args.output_html))

		parser.exit()

	parser.error("No actions specified")
