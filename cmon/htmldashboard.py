#!/usr/bin/env python3

"""Implementation of the `html_dashboard()` function."""

import logging
from pathlib import Path

import jinja2

from .dashboard import Dashboard

logger = logging.getLogger("output")

TEMPLATE_DIR = Path("templates")
DASHBOARD_TEMPLATE = Path("dashboard.html")

def html_dashboard(dashboard:Dashboard,
				   result:dict,
				   output:Path):

	template_dir = Path(__file__).parent.joinpath(TEMPLATE_DIR)
	template = jinja2.Template(template_dir.joinpath(DASHBOARD_TEMPLATE).open("r").read())
	h = output.open("w")
	context = {}
	context["dashboard"] = dashboard
	context["testsuites"] = {}
	for test_suite, test_suite_results in result.items():
		context["testsuites"][test_suite] = {}
		# context_test_suite = {}  # target : test : result
		for target in set(r[1] for r in test_suite_results):
			context["testsuites"][test_suite][target] = {}
			for (test, test_target), measurement in test_suite_results.items():
				if test_target is not target:
					continue

				context["testsuites"][test_suite][target][test] = measurement

	h.write(template.render(context))
	logger.info("Wrote {o}".format(o=output))
