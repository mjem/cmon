#!/usr/bin/env python3

"""Backend tests."""

import logging
from datetime import datetime
from datetime import timedelta

import sqlalchemy

from ..measurement import Measurement
from ..measurement import MeasurementState
from ..measurement import Message
from .backend import Backend
from ..context import Context

logger = logging.getLogger("database")

def measure_backend_db_tests(target:Backend, context:Context) -> Measurement:
	if len(target.db_tests) == 0:
		return Measurement(MeasurementState.NOT_APPLICABLE)

	database = target.database
	conn = database.connect()
	result = Measurement()
	for db_test in target.db_tests:
		bindvars = {
			"starttime": datetime.utcnow() - db_test.starttime_offset,
			"stoptime": datetime.utcnow(),
			"yesterday": datetime.utcnow().date() - timedelta(days=1),
			"yesterday1": datetime.utcnow().date() - timedelta(days=2),
		}
		cursor = conn.execute(sqlalchemy.text(db_test.sql), bindvars)
		row = cursor.fetchone()
		# logger.debug("result count " + str(result))
		if len(cursor.keys()) == 1:
			result_count = result[0]
			if row[0] >= db_test.min_count:
				result.add_child(
					Measurement(
						MeasurementState.GOOD,
						messages=[Message(db_test.name, row[0])]))

			else:
				result.add_child(
					Measurement(
						MeasurementState.FAILED,
						messages=[Message(db_test.name, "found {act} minimum {mn}".format(
							act=row[0], mn=db_test.min_count))]))

		else:
			new_measurement = Measurement(MeasurementState.GOOD)
			for cc, column_name in enumerate(cursor.keys()):
				new_measurement.add_message(db_test.name + '.' + column_name,
											row[cc])

			result.add_child(new_measurement)

	# Merge all the individual jobs query results into a single measurement
	result.traffic_lights()
	for child in result.children:
		result.messages.extend(child.messages)

	result.children = None
	return result

measure_backend_db_tests.label = "db_tests"
