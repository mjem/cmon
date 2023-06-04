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


		# activities:Iterable[str],
		# threshold:timedelta,
		# job_sidnum_filter:int=None):
@measure(
	label="Jobs",
	name="jobs",
	description="Scan jobs table for issues",
	subject_type=Backend,
	messages=[
		MessageDescription(
			name="recent",
			label="Most recent job",
			description="Age of most recently executed matching job",
			datatype=timedelta,
			multiple=dict),
		MessageDescription(
			name="failed",
			label="Failed jobs",
			description="Count of recent failed jobs",
			datatype=timedelta,
			multiple=dict),
		MessageDescription(
			name="errors",
			label="Log file errors",
			description="Total logged errors for recent jobs",
			datatype=timedelta,
			multiple=dict),
	]
)
def measure_backend_jobs(subject:Backend, context:Context):
	conn = subject.database.connect()
	result = Measurement(state=MeasurementState.GOOD)
	for expected_jobs in subject.expected_jobs:
		where_clauses = []
		bindvars = {}
		for f in expected_jobs["filters"]:
			where_clauses.append(f)

		where_clauses.append("activity=:activity")
		bindvars["activity"] = expected_jobs["activity"]

		sql = "SELECT max({field}) FROM jobs WHERE {where}".format(
			field=expected_jobs["field"],
			where=" AND ".join(where_clauses))
	# bindvars["sidnum"] = job_sidnum_filter
		cursor = conn.execute(sqlalchemy.text(sql), bindvars)
		last_gen_time = cursor.fetchone()[0]
		logger.info('last gen time {l}'.format(l=last_gen_time))

		# delay = datetime.utcnow() - last_gen_time

		result.add_message(
			Message(name="recent",
					parameter=expected_jobs["activity"],
					value=last_gen_time),
			)

		cursor.close()

	conn.close()
	# activity_clauses = []
	# for a in activities:
	# 	where_clauses.append("jobs.gen_time>:mintime")
	# 	bindvars["mintime"] = datetime.utcnow() - threshold

	# 	if len(where_clauses) == 0:
	# 		where = ""

	# 	else:
	# 		where = " WHERE {clauses}".format(clauses=" AND ".join(where_clauses))

	# 	sql = "SELECT jobs.id, processes.execute_stop, jobs.status FROM processes, jobs{where}".format(where=where)
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
		# cursor = conn.execute(sqlalchemy.text(sql), bindvars)


	
	return result

