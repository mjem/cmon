#!/usr/bin/env python3

"""Implementation of Database class."""

from enum import Enum
from typing import Iterable

try:
	import psycopg2
except ImportError:
	psycopg2 = None

from ..testable import Testable
from ..server.server import Server

class DatabaseType(Enum):
	POSTGRES = "postgres"

class DatabaseNoAuth(Exception):
	pass

class Database(Testable):
	"""Representation of a database to be tested."""
	def __init__(self,
				 servertype:DatabaseType,
				 host:Server,
				 label:str=None,
				 database:str=None,
				 port:int=None,
				 user:str=None,
				 password:str=None):
		super().__init__(label=label)
		self.servertype = servertype
		self.host = host
		self.database = database
		self.port = port
		self.user = user
		self.password = password
		self.connection = None

	def connect(self) -> object:
		"""Log into database.

		Raises:
		IOError if local file cannot be found
		ConnectionException for network or port errors
		DatabaseNoAuth for authentication errors
		DatabaseError if database is not acception connections or local file is bad
		"""
		if self.servertype is DatabaseType.POSTGRES:
			return self.connect_postgres()

		raise NotImplementedError()

	def connect_postgres(self) -> "psycopg2.extensions.connection":
		if self.connection is None:
			self.connection = psycopg2.connect(database=self.database,
											   user=self.user,
											   password=self.password,
											   host=self.host.hostname,
											   port=self.port)
		return self.connection

	def links(self) -> Iterable[Testable]:
		"""Return our linked items for dashboard display."""
		if self.host is not None:
			return [self.host]

		else:
			return []
