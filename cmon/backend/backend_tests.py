#!/usr/bin/env python3

"""Backend tests."""

import logging
from datetime import datetime

import sqlalchemy

from ..measurement import Measurement
from ..measurement import MeasurementState
from ..measurement import Message
from .backend import Backend
from ..context import Context

logger = logging.getLogger("database")

def measure_backend_jobs(target:Backend, context:Context) -> Measurement:
	if len(target.jobs) == 0:
		return Measurement(MeasurementState.NOT_APPLICABLE)

	database = target.database
	conn = database.connect()
	# cur = conn.cursor()
	result = Measurement()
	for job in target.jobs:
		clauses = ["gen_time>:min_time"]
		bindvars = {"min_time": datetime.utcnow() - job.period}
		if job.activity is not None:
			# clauses.append("activity in :activities")
			clauses.append("activity = ANY(:activities)")
			if isinstance(job.activity, tuple):
				bindvars["activities"] = job.activity

			else:
				bindvars["activities"] = job.activity

		sql = "SELECT count(*) FROM jobs WHERE {where}".format(
			where=" AND ".join(clauses))
		logger.debug(sql + " " + str(bindvars))
		# cur.execute(sql, bindvars)
		cursor = conn.execute(sqlalchemy.text(sql), bindvars).fetchone()
		job_count = cursor[0]
		logger.debug("job count " + str(job_count))
		result.add_child(
			Measurement(
				MeasurementState.GOOD if job_count>=job.min_count else \
				MeasurementState.FAILED,
				messages=[Message(job.message(), job_count)]))
		# print("jobs result", result)

	# Merge all the individual jobs query results into a single measurement
	result.traffic_lights()
	for child in result.children:
		result.messages.extend(child.messages)

	result.children = None
	# result.add_message("one", 10)
	return result

measure_backend_jobs.label = "jobs"

def measure_backend_ingestion():
	raise NotImplementedError()

def measure_backend_events():
	raise NotImplementedError()

def measure_backend_ts():
	raise NotImplementedError()

def measure_backend_reports():
	raise NotImplementedError()
