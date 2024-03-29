#!/usr/bin/env python3

"""Implementation of Database class."""

import logging
from enum import Enum
from typing import Iterable

import sqlalchemy

from ..testable import Testable
from ..server.server import Server

logger = logging.getLogger("database")

DIALECTS = (
	'postgresql',
)

class CannotConnect(Exception):
	pass

class DatabaseNoAuth(Exception):
	pass

class Database(Testable):
	"""Representation of a database to be tested."""
	name = "database"
	label = "Database"
	description = "Representation of a database server"

	def __init__(self,
				 dialect:str,
				 host:Server,
				 label:str,
				 database:str=None,
				 port:int=None,
				 user:str=None,
				 password:str=None):
		"""Args:
		`dialect`: sqlalchemy dialect string e.g. "postgresql", "postgresql+psycop"
		`host`:
		`database`: Database name
		`port`: If non standard
		`user`: Username
		`password`: Password if not configured in ~/.pgppass or other standard place
		"""
		super().__init__(label=label)
		# Use psycopg3 instead of the default psycopg2
		# might give better performance but beware of errors on shutdown
		# on opensuse / python3.9 system
		# if dialect == "postgresql":
			# dialect = "postgresql+psycopg"

		self.dialect = dialect
		self.host = host
		self.database = database
		self.port = port
		self.user = user
		self.password = password
		self.engine = None
		self.connection = None

	def __del__(self):
		if self.connection is not None:
			self.connection.rollback()
			del self.connection

	def dsn(self):
		return "{dialect}://{user}{password}@{host}{port}/{name}".format(
			dialect=self.dialect,
			user=self.user,
			password="" if self.password is None else ":{password}".format(
				password=self.password),
			host=self.host.hostname,
			port="" if self.port is None else ":{port}".format(port=self.port),
			name=self.database)

	def connect(self) -> object:
		"""Log into database.

		Raises:
		IOError if local file cannot be found
		ConnectionException for network or port errors
		DatabaseNoAuth for authentication errors
		DatabaseError if database is not acception connections or local file is bad
		"""
		# sqlalchemy.create_engine("postgresql+psycopg://chartjcs_enduser@localhost/chartjcs")
		# sqlalchemy.create_engine("postgresql://chartjcs_enduser@localhost/chartjcs")
		# metadata_obj=sqlalchemy.MetaData()
		# tm = sqlalchemy.Table("tm", metadat_obj, autoload_with=engine)
		# conn.execute(sqlalchemy.text("select 140")).fetchall()[0][0]
		if self.connection is None:
			dsn = self.dsn()
			logger.info("Database string {dsn}".format(dsn=dsn))
			self.engine = sqlalchemy.create_engine(dsn, echo=True)
			try:
				self.connection = self.engine.connect()
			except sqlalchemy.exc.OperationalError:
				raise CannotConnect("Connection to {db} failed".format(db=self.dsn()))

		return self.connection

	def links(self) -> Iterable[Testable]:
		"""Return our linked items for dashboard display."""
		if self.host is not None:
			return [self.host]

		else:
			return []
