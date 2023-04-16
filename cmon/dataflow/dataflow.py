#!/usr/bin/env python3

"""Implementation of Dataflow class."""

from pathlib import Path
from datetime import timedelta
from typing import Iterable

from ..testable import Testable
from ..server.server import Server

class Dataflow(Testable):
	name = "dataflow"
	label = "Dataflow"
	description = "Representation of a flow of data into a directory tree"

	def __init__(self,
				 label:str,
				 directory: Path,
				 server:Server=None,
				 pattern:str=None,
				 max_outage: timedelta=None,
				 important:bool=True):
		"""
		Args:
		- `directory`: Directory name to test
		- `server`: Server to ssh into before checking, if needed
		- `pattern`: Filter files by wildcard
		- `max_outage`: Only raise an error if no changes within time frame
		- `label`: Nice name for this flow
		"""
		super(Dataflow, self).__init__(label=label, important=important)
		self.directory = directory
		self.server = server
		self.pattern = pattern
		self.max_outage = max_outage

	def links(self) -> Iterable[Testable]:
		"""Return our linked items for dashboard display."""
		if self.server is not None:
			return [self.server]

		else:
			return []
