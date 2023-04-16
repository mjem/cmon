#!/usr/bin/env python3

"""Backend tests."""

import logging
from datetime import datetime
from datetime import timedelta
from typing import Iterable

import sqlalchemy

from ..measurement import Measurement
from ..measurement import MeasurementState
from ..measurement import MessageDescription
from ..measurement import Message
from ..measurement import measure
from .backend import Backend
from ..context import Context

logger = logging.getLogger("database")

# Ingestion jobs check over timerange:
#  - max latency -> threshold
#  - avg latency -> max threshold
#  - failed jobs
#  - max errors -> max threshhold
#  - total jobs -> min threshold

# Generic jobs check over timerange:
#  - failed jobs
#  - max errors -> max threshold
#  - total jobs -> min threshold

# Reports check

# Events check

# Timeseries check


def measure_backend_recent_job(
		activities:Iterable[str],
		threshold:timedelta,
		job_sidnum_filter:int=None):
	"""Basic jobs check, throw error if no job within timerange
	"""
	@measure(
		name="recentjob",
		label="Recent jobs",
		description="Check jobs have been successfully executed without recent time limit",
		subject_type=Backend,
		messages=[
			MessageDescription(
				name="recent",
				label="Most recent job",
				description="Age of most recently executed matching job",
				datatype=timedelta)
		]
	)
	def imp(subject:Backend, context:Context) -> Measurement:
		conn = subject.database.connect()
		result = Measurement()
		where_clauses = []
		bindvars = {}
		if job_sidnum_filter is not None:
			where_clauses.append("jobs.sid_num=:sidnum")
			bindvars["sidnum"] = job_sidnum_filter

		# where_clauses.append("jobs.activity in :activities")
		# bindvars["activities"] = tuple(activities)
		activity_clauses = []
		for a in activities:
			bindvars["activity{cc}".format(cc=len(activity_clauses))] = a
			activity_clauses.append("jobs.activity=:activity{cc}".format(cc=len(activity_clauses)))

		where_clauses.append("({clauses})".format(clauses=" OR ".join(activity_clauses)))

		where_clauses.append("jobs.process_id=processes.id")

		where_clauses.append("jobs.gen_time>:mintime")
		bindvars["mintime"] = datetime.utcnow() - threshold

		if len(where_clauses) == 0:
			where = ""

		else:
			where = " WHERE {clauses}".format(clauses=" AND ".join(where_clauses))

		sql = "SELECT jobs.id, processes.execute_stop, jobs.status FROM processes, jobs{where}".format(where=where)
		# sql="SELECT min(latency) min,avg(latency) avg,max(latency) max "\
			# "FROM "\
			# "(SELECT p.execute_stop-j.sensing_start AS latency FROM jobs j, processes p "\
			# "WHERE j.process_id=p.id AND j.activity='TM_INGESTER' AND j.sid_num=1 and "\
			# "j.sensing_start BETWEEN :yesterday1 AND :yesterday) a",
		# ),
		# bindvars = {
			# "starttime": datetime.utcnow() - starttime_offset,
			# "stoptime": datetime.utcnow(),
			# "yesterday": datetime.utcnow().date() - timedelta(days=1),
			# "yesterday1": datetime.utcnow().date() - timedelta(days=2),
		# }
		cursor = conn.execute(sqlalchemy.text(sql), bindvars)

		most_recent = None

		result = Measurement(MeasurementState.GOOD)
		for job_id, execution_stop, status in cursor:
			if status != "COMPLETED":
				result.add_message(Message("recent", error="Job {id} failed".format(id=job_id)))
				result.state = MeasurementState.FAILED
				return result

			if most_recent is None:
				most_recent = execution_stop

			else:
				most_recent = max(most_recent, execution_stop)

		if most_recent is None:
			result.add_message(Message("recent", error="No recent jobs"))
			result.state = MeasurementState.FAILED
			return result

		# row = cursor.fetchone()
		# for cc, column_name in enumerate(cursor.keys()):
			# result.add_message(name + '.' + column_name, row[cc])
			# if row[cc] and row[cc] < min_count:
		# result.state = MeasurementState.FAILED

		result.add_message(Message("recent", most_recent))

		return result

	# imp.label = label
	# imp.decorator = measure_backend_job_latency.decorator
	return imp
