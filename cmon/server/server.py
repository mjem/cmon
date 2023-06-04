#!/usr/bin/env python3

"""Implementation of Server class."""

import logging
from typing import Dict
from typing import Optional
from typing import Union
from typing import Iterable

import paramiko

from ..testable import Testable
from ..mount import Mount
from ..utils import is_listlike

# paramiko is very verbose on the debug level
logging.getLogger("paramiko").setLevel(logging.WARNING)
logger = logging.getLogger("server")

class ConnectionException(Exception):
	"""Network cannot find required server."""
	pass

class Server(Testable):
	"""Representation of a server which can be tested."""
	name = "server"
	label = "Server"
	description = "Representation of a single server which can host services"

	def __init__(self,
				 hostname:str,
				 label:str,
				 name:str=None,
				 description:str=None,
				 ssh_user:str=None,#1Union[str,Iterable[str]]=None,
				 ssh_hack:str=None,
				 # ssh_password:str=None,
				 # ssh_config:Union[str, Iterable[str]]=None,
				 mounts:Iterable[Mount]=None,
				 important:bool=True,
				 docker_containers:Iterable[str]=None):
		"""
		Args:
		- `hostname`: Network hostname for connections
		- `label`: Nice name for this server
		- `ssh_user`: Username to attempt for ssh connection(s)
		- `ssh_config`: Entry in ssh config file to read connection information(s) from
		- `mounts`: Mounted directories for testing
		- `important`: If the server is not `important` then a test failure in this server does not
			result in the whoel test suite failing
		"""
		super().__init__(label=label,
						 name=name,
						 description=description,
						 important=important)
		self.hostname = hostname
		# if ssh_user is None:
			# self.ssh_user = []

		# elif is_listlike(ssh_user):
			# self.ssh_user = ssh_user

		# else:
			# self.ssh_user = [ssh_user]

		# if ssh_config is None:
			# self.ssh_config = []

		# elif is_listlike(ssh_config):
			# self.ssh_config = []

		# else:
			# self.ssh_config = [ssh_config]

		self.ssh_user = ssh_user
		self.ssh_hack = ssh_hack

		self.mounts = mounts
		self.ssh_user_client = None
		# self.ssh_user_clients = {}
		# self.ssh_config_clients = {}
		self.docker_containers = docker_containers
		# self.ssh_password = ssh_password

	def __str__(self):
		if self.label:
			return "Server {label}".format(label=self.label)

		else:
			return "Server"

	# def ssh_connect_imp(self,
	# 					hostname,
	# 					username):
	# 	"""SSH connection implementation."""
	# 	result = paramiko.client.SSHClient()
	# 	result.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	# 	try:
	# 		logger.info("ssh connect to {host} as {user}".format(host=hostname, user=username))
	# 		result.connect(hostname, username=username)
	# 	except paramiko.ssh_exception.AuthenticationException as e:
	# 		raise ConnectionException(str(e)) from e

	# 	return result

	# def ssh_connect_user(self,
	# 					 ssh_user:str):
	# 	"""SSH connection using our `hostname` and a given `ssh_user`, cached."""
	# 	if ssh_user not in self.ssh_user_clients:
	# 		self.ssh_user_clients[ssh_user] = self.ssh_connect_imp(hostname=self.hostname,
	# 															   username=ssh_user)

	# 	return self.ssh_user_clients[ssh_user]

	# def ssh_connect_config(self,
	# 					   ssh_config:str):
	# 	"""SSH connection using a named ssh config file specification, cached."""
	# 	raise NotImplementedError()

	def ssh_connect(self,
					# ssh_user:str=None,
					# ssh_config:str=None
					# ) -> Optional[paramiko.client.SSHClient]:
					) -> paramiko.client.SSHClient:
		"""Return an ssh connection.

		With no paramereters the best connection is selected.

		If either `ssh_config` (from ssh config file) or `ssh_user` (Unix username) are given
		this is used instead.
		An `ssh_config` option could even override the hostname, for single servers
		with multiple hostnames.

		"""
		# allow forced read of config information from ssh config file
		# if ssh_config is not None:
		# 	return self.ssh_connect_config(ssh_config)

		# # allow forced ssh username
		# if ssh_user is not None:
		# 	return self.ssh_connect_user(ssh_user)

		# # fail by returning a null if we have no ssh config information
		# # (add test of ssh_config when implemented)
		# if len(self.ssh_config) > 0:
		# 	return self.ssh_connect_config(self.ssh_config[0])

		# # use first defined `ssh_user`
		# if len(self.ssh_user) > 0:
		# 	return self.ssh_connect_user(self.ssh_user[0])

		# return None

		if self.ssh_user is None:
			# no ssh connection configured
			return None

		# cached failure
		if self.ssh_user_client is False:
			return None

		if self.ssh_user_client is not None:
			return self.ssh_user_client

		result = paramiko.client.SSHClient()
		# result.load_system_host_keys()
		result.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		# pkey = paramiko.RSAKey.from_private_key_file("/tcenas/home/elson/.ssh/id_rsa")
		try:
			logger.info("ssh connect as {user} to {host}".format(host=self.hostname, user=self.ssh_user))
			if self.ssh_hack is None:
				result.connect(self.hostname, username=self.ssh_user)

			elif self.ssh_hack == "disabled_algorithms_pubkeys_rsa_sha2_256_rsa_sha2_512":
				result.connect(self.hostname,
							   username=self.ssh_user,
							   disabled_algorithms={'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']})

				# , pkey=pkey)
			# , look_for_keys=False)

		except paramiko.ssh_exception.AuthenticationException as e:
			logger.warn("ssh connect failed {e}".format(e=e))
			self.ssh_user_client = False
			raise ConnectionException(str(e)) from e

		self.ssh_user_client = result
		return result

	def get_id(self) -> str:
		if self.name:
			return self.name

		return self.hostname
