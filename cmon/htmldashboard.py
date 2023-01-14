#!/usr/bin/env python3

"""Implementation of the `html_dashboard()` function."""

import logging
from pathlib import Path
import shutil
from typing import Iterable
from typing import Dict

import jinja2

from .dashboard import Dashboard
from .measurement import Measurement
from .measurement import MeasurementState

logger = logging.getLogger("output")

HERE = Path(__file__).parent
TEMPLATE_DIR = HERE.joinpath("templates")
THIRDPARTY_DIR = HERE.joinpath("3rdparty")

class Theme:
	"""Configuration for dashboard function."""
	def __init__(self,
				 top_template:Path,
				 top_output:Path,
				 statics:Iterable[Path]=[],
				 states:Dict[MeasurementState,str]={}):
		self.top_template = top_template
		self.top_output = top_output
		self.statics = statics
		self.states = states

# HTML web output theme based around bootstrap
bootstrap_theme = Theme(
	top_template=TEMPLATE_DIR.joinpath("dashboard.html"),
	top_output=Path("index.html"),
	statics=(
		THIRDPARTY_DIR.joinpath("bootstrap-5.3.0-alpha1-dist/css/bootstrap.min.css"),
		THIRDPARTY_DIR.joinpath("bootstrap-5.3.0-alpha1-dist/js/bootstrap.min.js"),
	),
	states={
		MeasurementState.GOOD: "badge rounded-pill text-bg-success",
	}
)

def html_dashboard(dashboard_result:Measurement,
				   output_dir:Path,
				   theme:Theme=bootstrap_theme):
	output_dir.mkdir(exist_ok=True)
	for static in theme.statics:
		shutil.copy(static, output_dir)

	template = jinja2.Template(theme.top_template.open("r").read())
	top_output = output_dir.joinpath(theme.top_output)
	h = top_output.open("w")
	context = {"dashboard_result": dashboard_result,
			   "theme": theme}
	h.write(template.render(context))
	logger.info("Wrote {o}".format(o=top_output))
