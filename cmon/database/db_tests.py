#!/usr/bin/env python3

"""Implementation of database tests."""

from ..context import Context
from .database import Database
from ..measurement import Measurement

def measure_db_login(target:Database, context:Context):
	"""Check we can log into databaseand record server info."""
	connection = target.connect()
	return Measurement("GOOD")

def measure_db_size():
	"""Measure the total used size of database."""
	raise NotImplementedError()
