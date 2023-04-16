#!/usr/bin/env python3

"""Implementation of database tests."""

from ..context import Context
from .database import Database
from ..measurement import Measurement
from ..measurement import measure

# pg_size_pretty(pg_database_size('chartmtg'));


@measure(
	label="Database login",
	name="login",
	description="Check we can log into the server",
	subject_type=Database)
def measure_db_login(subject:Database, context:Context):
	"""Check we can log into databaseand record server info."""
	connection = subject.connect()
	return Measurement("GOOD")

@measure(
	label="Database size",
	name="size",
	description="Read database size",
	subject_type=Database)
def measure_db_size():
	"""Measure the total used size of database."""
	raise NotImplementedError()
