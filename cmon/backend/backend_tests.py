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

def measure_backend_sql(
		name,
		sql:str,
		label:str=None,
		starttime_offset:timedelta=timedelta(),
		min_count:int=1,
		description:str=None):
	"""Make a configurable generic SQL query measurement.

	Args:
	- `name`: Internal function name for storage
	- `sql`: SQL statement to run
	- `label`: Display label for UI
	- `description`: Long description if the user requests

	If a single value is returned, that is xxx.
	If multiple values are returned, they should be aliased, and will become measurement
	messages.

	Hide messages (not important) by prefixing the alias with '_'.
	"""
	def imp(target:Backend, context:Context) -> Measurement:
		conn = target.database.connect()
		result = Measurement()
		bindvars = {
			"starttime": datetime.utcnow() - starttime_offset,
			"stoptime": datetime.utcnow(),
			"yesterday": datetime.utcnow().date() - timedelta(days=1),
			"yesterday1": datetime.utcnow().date() - timedelta(days=2),
		}
		cursor = conn.execute(sqlalchemy.text(sql), bindvars)
		row = cursor.fetchone()
		result = Measurement(MeasurementState.GOOD)
		for cc, column_name in enumerate(cursor.keys()):
			result.add_message(name + '.' + column_name, row[cc])
			if row[cc] and row[cc] < min_count:
				result.state = MeasurementState.BAD

		return result

	imp.label = label
	return imp
