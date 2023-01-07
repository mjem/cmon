#!/usr/bin/env python3

import argparse
import runpy

from .log import init_log
from .printer import Printer
from .context import Context

def main():
	init_log()
	parser = argparse.ArgumentParser()
	parser.add_argument("--show",
						action="store_true",
						help="Show current configuration to console")
	parser.add_argument("--simulate",
						action="store_true",
						help=("Pretend to execute all measurements in the dashboard, "
							  "logging actions and validating configuration"))
	parser.add_argument("--run",
						action="store_true",
						help="Run test suites")
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
	if args.config_py:
		config = runpy.run_path(args.config_py)#, init_globals=globals()))
		dashboard = config["dashboard"]

	if config is None:
		parser.error("No configuration file given")

	if args.show:
		dashboard.show(Printer())
		parser.exit()

	context=Context(simulate=args.simulate,
					verbose=args.verbose)

	if args.simulate:
		dashboard.run(context)
		parser.exit()

	if args.run:
		dashboard.run(context)
		parser.exit()

	parser.error("No actions specified")
