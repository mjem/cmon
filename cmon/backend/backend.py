#!/usr/bin/env python3

"""Implementation of Backend class."""

from datetime import timedelta
from typing import Iterable
from typing import Union

import humanize

from ..database.database import Database
from ..dataflow.dataflow import Dataflow
from ..server.server import Server
from ..testable import Testable
from ..utils import is_listlike

# class DatabaseConnectionMethod
# direct
# ssh
# api

class BackendJobsTest:
	def __init__(self,
				 period:timedelta=timedelta(hours=1),
				 activity:Union[str, Iterable[str]]=None,
				 min_count:int=1,
				 description:str=None):
		self.period = period
		if activity is None:
			self.activity = None

		elif is_listlike(activity):
			self.activity = activity

		else:
			self.activity = [activity]

		self.min_count = min_count
		self.description = description

	def message(self) -> str:
		"""Text to put into jobs test message."""
		if self.description is not None:
			return self.description

		return "Jobs {jobs} in {dur}".format(
			min=self.min_count,
			jobs=",".join(self.activity),
			dur=humanize.naturaldelta(self.period))

class Backend(Testable):
	"""Representation of a CHART environment processing backend."""

	def __init__(self,
				 database:Database=None,
				 server:Server=None,
				 dataflows: Iterable[Dataflow]=None,
				 jobs: Union[BackendJobsTest, Iterable[BackendJobsTest]]=None,
				 # events=None,
				 # reports=None,
				 # timeseries_ap=None,
				 # timeseries_pus_stats=None,
				 label:str=None,
				 important:bool=True,
				 description:str=None):
		super().__init__(label=label, description=description, important=important)
		self.database = database
		self.server = server
		if dataflows is None:
			self.dataflows = []

		elif is_listlike(dataflows):
			self.dataflows = dataflows

		else:
			self.dataflows = [dataflows]

		if jobs is None:
			self.jobs = []

		elif is_listlike(jobs):
			self.jobs = jobs

		else:
			self.jobs = [jobs]

		# self.events = events
		# self.reports = reports
		# self.timeseries_ap = timeseries_ap
		# self.timeseries_pus_stats = timeseries_pus_stats

	def links(self) -> Iterable[Testable]:
		result = []
		if self.server is not None:
			result.append(self.server)

		result.extend(self.dataflows)
		if self.database is not None:
			result.append(self.database)

		return result
