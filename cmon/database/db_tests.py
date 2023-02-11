#!/usr/bin/env python3

"""Implementation of database tests."""

from ..context import Context
from .database import Database
from ..measurement import Measurement

# pg_size_pretty(pg_database_size('chartmtg'));


def measure_db_login(target:Database, context:Context):
	"""Check we can log into databaseand record server info."""
	connection = target.connect()
	return Measurement("GOOD")

measure_db_login.name = "login"
measure_db_login.label = "Login"

def measure_db_size():
	"""Measure the total used size of database."""
	raise NotImplementedError()

measure_db_size.label = "sizes"
