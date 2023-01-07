#!/usr/bin/env python3

"""Implementation of Dataflow class."""

from pathlib import Path
from datetime import timedelta

from ..testable import Testable
from ..server.server import Server

class Dataflow(Testable):
	def __init__(self,
				 directory: Path,
				 server:Server=None,
				 pattern:str=None,
				 max_outage: timedelta=None,
				 label:str=None):
		"""
		Args:
		- `directory`: Directory name to test
		- `server`: Server to ssh into before checking, if needed
		- `pattern`: Filter files by wildcard
		- `max_outage`: Only raise an error if no changes within time frame
		- `label`: Nice name for this flow
		"""
		super(Dataflow, self).__init__(label=label)

