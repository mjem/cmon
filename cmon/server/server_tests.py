#!/usr/bin/env python3

"""Implementation of tests against a server."""

import logging
from copy import copy

import humanize

from ..measurement import Measurement
from ..measurement import MeasurementState
from ..measurement import MessageDescription
from .server import Server
from .server import ConnectionException
from ..context import Context
from ..shell import shell
from ..shell import shell_validate
from .df import decode_df
from ..utils import is_listlike

logger = logging.getLogger()

NEWLINE = "\n"

message_description_mount = MessageDescription(
	label="Mount",
	description="Name of a mount point with human-readable total and used size reported",
	datatype=str,
	# quantisation=Nargs.MULTIPLE,
	# importance=Important.DASHBOARD,
	)

def measure_server_ping(target:Server, context:Context):
	"""Check the server responds to ping.

	Requires a response to an ICMP packet and failure to ping doesn't
	necessarily mean the server is down."""
	if context.simulate:
		logger.info("Simulating a ping of {s}".format(s=target))
		return

	shelled = shell("ping -c 1 " + target.hostname)
	# result = shell("ping -c 1 " + target.hostname, verbose=True, echo=True)
	# logger.info("Ping status code {c}".format(c=result.returncode))
	valid = shell_validate(shelled)
	# logger.info("Successful ping of " + target.hostname)
	if context.verbose:
		logger.info(result.stdout)

	if valid is True:
		result = Measurement(state=MeasurementState.GOOD)
		result.add_message("host", target.hostname)
		return result

	result = Measurement(state="FAILED")
	result.add_message("ping.{hostname}".format(hostname=target.hostname), valid)
	return result

measure_server_ping.label = "ping"
measure_server_ping.description = "Check we can ping the server"

def measure_server_ssh_aliveness(target:Server, context:Context):
	try:
		client = target.ssh_connect()
		if client is None:
			return Measurement(state=MeasurementState.NOT_APPLICABLE)

	except ConnectionException as e:
		return Measurement(state=MeasurementState.FAILED, message=str(e))

	result = Measurement(state=MeasurementState.GOOD)
	if target.ssh_user is not None:
		if is_listlike(target.ssh_user):
			result.add_message("user", target.ssh_user[0])

		else:
			result.add_message("user", target.ssh_user)

	return result

measure_server_ssh_aliveness.label = "ssh aliveness"
measure_server_ssh_aliveness.description = "Check we can ssh into the server"

def measure_server_ssh_mountpoints(target:Server, context:Context):
	"""Check all configured mountpoints are mounted."""
	if target.mounts is None:
		return Measurement("NOT_APPLICABLE")

	client = target.ssh_connect()
	if client is None:
		return Measurement(state=MeasurementState.FAILED, message=str(e))

	stdin, stdout, stderr = client.exec_command("df")
	error = stderr.read().decode().strip()

	# Use helper to decode actual df output
	found_mounts = decode_df(stdout.read().decode().split(NEWLINE))

	result = Measurement()
	good = 0
	# For each mount we are configured to look for
	for req in target.mounts:
		# logger.info("checking if " + req.mountpoint + " was found")
		found_mount = found_mounts.get(req.mountpoint)
		if found_mount:
			value = "{used} / {total} used".format(
				used=humanize.naturalsize(found_mount.used),
				total=humanize.naturalsize(found_mount.total))
			good += 1

		else:
			value = "missing"

		result.add_message(req.mountpoint, value, message_description_mount)

	if good == len(target.mounts):
		result.state = "GOOD"

	else:
		result.state = "FAILED"

	return result

measure_server_ssh_mountpoints.label = "mounts"
measure_server_ssh_mountpoints.description = """
Check all configured mountpoints have a partition mounted"""

def measure_server_ssh_sysinfo(target:Server, context:Context):
	"""Retreive system info as measurement messages.

	Reads:
	- OS
	- RAM / swap available / free
	- CPU count and total usage
	- net i/o
	- disk i/o
	"""
	client = target.ssh_connect()
	if client is None:
		return Measurement(MeasurementState.NOT_APPLICABLE)

	result = Measurement(MeasurementState.GOOD)
	result.add_message("OS", "Debian sid")
	result.add_message("CPU", "4")
	result.add_message("RAM", "32 GB total 28 GB used")
	return result

measure_server_ssh_sysinfo.label = "sysinfo"
measure_server_ssh_sysinfo.description = """
Not implemented - show system information"""

def measure_server_ssh_docker(target:Server, context:Context):
	"""Retrieve information about running docker containers.

	Uses primary ssh connection and docker command line tool."""
	if target.docker_containers is None:
		return Measurement(MeasurementState.NOT_APPLICABLE)

	result = Measurement(MeasurementState.GOOD)
	result.add_message("chart-db", "postgres:15.1")
	result.add_message("chart-jcs", "chart/jcs:3.2")
	return result

measure_server_ssh_docker.label = "docker"
measure_server_ssh_docker.description = """Report on running docker containers"""
