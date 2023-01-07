#!/usr/bin/env python3

"""Implementation of Backend class."""

from typing import Iterable
from typing import Union

from .activity import Activity
from ..database.database import Database
from ..dataflow.dataflow import Dataflow
from ..server.server import Server
from ..testable import Testable


class CHARTBackend(Testable):
	"""Representation of a CHART environment processing backend."""

	def __init__(self,
				 database: Union[Iterable[Database], Database] = None,
				 server: Server = None,
				 dataflows: Iterable[Dataflow] = None,
				 jobs: Iterable[Activity] = None,
				 events = None,
				 reports = None,
				 timeseries_ap = None,
				 timeseries_pus_stats = None,
				 label: str = None):
		super().__init__(label=label)
		self.database = database
		self.server = server
		self.dataflows = dataflows
		self.jobs = jobs
		self.events = events
		self.reports = reports
		self.timeseries_ap = timeseries_ap
		self.timeseries_pus_stats = timeseries_pus_stats
