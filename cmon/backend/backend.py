#!/usr/bin/env python3

"""Implementation of Backend class."""

from typing import Iterable

from ..database.database import Database
from ..dataflow.dataflow import Dataflow
from ..measurement import Measurement
from ..server.server import Server
from ..testable import Testable
from ..utils import is_listlike

# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
    # from


# class DatabaseConnectionMethod
# direct
# ssh
# api

# class BackendDb:
	# def __init__(self,
				 # name:str,
				 # sql:str,
				 # starttime_offset:timedelta=timedelta(),
				 # min_count:int=1,
				 # label:str=None):
		# self.name = name
		# self.sql = sql
		# self.starttime_offset = starttime_offset
		# self.min_count = min_count
		# self.label = label


class Backend(Testable):
	"""Representation of a CHART environment processing backend."""
	name = "backend"
	label = "Backend"
	description = ("Representation of backend processing software optionally using a databasse and "
				   "providing a website")

	def __init__(self,
				 database: Database = None,
				 server: Server = None,
				 dataflows: Iterable[Dataflow] = None,
				 # jobs: Union[BackendJobsTest, Iterable[BackendJobsTest]]=None,
				 # events: Iterable[BackendEvents]=[],
				 # flows: Iterable[BackendFlow]=[],
				 # db_tests: Iterable[BackendDb]=[],
				 label: str = None,
				 important: bool = True,
				 description: str = None,
				 tests: Iterable[Measurement] = None):
		super().__init__(label=label, description=description, important=important, tests=tests)
		self.database = database
		self.server = server
		if dataflows is None:
			self.dataflows = []

		elif is_listlike(dataflows):
			self.dataflows = dataflows

		else:
			self.dataflows = [dataflows]

		# if jobs is None:
			# self.jobs = []

		# elif is_listlike(jobs):
			# self.jobs = jobs

		# else:
			# self.jobs = [jobs]

		# self.flows = flows
		# self.db_tests = db_tests
		# self.events = events
		# self.reports = reports
		# self.timeseries_ap = timeseries_ap
		# self.timeseries_pus_stats = timeseries_pus_stats

	def links(self) -> Iterable[Testable]:
		"""Return a list of other objects that we rely on."""
		result = []
		if self.server is not None:
			result.append(self.server)

		result.extend(self.dataflows)
		if self.database is not None:
			result.append(self.database)

		return result
