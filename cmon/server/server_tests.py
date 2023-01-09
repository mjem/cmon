#!/usr/bin/env python3

"""Implementation of tests against a server."""

import logging
from copy import copy

from ..measurement import Measurement
from ..measurement import MeasurementState
from .server import Server
from .server import ConnectionException
from ..context import Context
from ..shell import shell
from ..shell import shell_validate

logger = logging.getLogger()

NEWLINE = "\n"

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
		return Measurement(state=MeasurementState.GOOD)

	result = Measurement(state="FAILED")
	result.add_message("ping.{hostname}".format(hostname=target.hostname), valid)
	return result

measure_server_ping.label = "ping"

def measure_server_ssh_aliveness(target:Server, context:Context):
	try:
		client = target.ssh_connect()
		if client is None:
			return Measurement(state=MeasurementState.NOT_APPLICABLE)

	except ConnectionException as e:
		return Measurement(state=MeasurementState.FAILED, message=str(e))

	return Measurement(state=MeasurementState.GOOD)

measure_server_ssh_aliveness.label = "aliveness"

def measure_server_ssh_mountpoints(target:Server, context:Context):
	"""Check all configured mountpoints are mounted."""
	if target.mounts is None:
		return Measurement("NOT_APPLICABLE")

	# required_mounts = copy(target.mounts)
	# for mount in target.mounts:
		# logger.info("Checking for mount " + mount.mountpoint)

	client = target.ssh_connect()
	if client is None:
		return Measurement(state=MeasurementState.FAILED, message=str(e))

	stdin, stdout, stderr = client.exec_command("df")
	# out = stdout.read().decode().strip()
	error = stderr.read().decode().strip()
	# logger.info("Ran df")
	# logger.info("Got stdout " + out)
	# logger.info("Got stderr len " + str(len(error)))# + " text " + error)
	mount_column = None
	found_mounts = []
	for line in stdout.read().decode().split(NEWLINE):
		if len(line) == 0:
			continue

		cells = line.split()
		if mount_column is None:
			# first line
			for cc, heading in enumerate(cells):
				# logger.info("CELL " + heading)
				if "mount" in heading.lower():
					# logger.info("Got mount column as {cc}".format(cc=cc))
					mount_column = cc

			if mount_column is None:
				return Measurement(state="ERROR", message="Could not decode df header " + line)

			continue

		# logger.info("LINE: " + line)
		mountpoint = cells[mount_column]
		found_mounts.append(mountpoint)
		# logger.info("Identified mount point " + mountpoint)

		# purge = []
		# for req in required_mounts:
			# if req.mountpoint == mountpoint:
				# logger.info("Requirement {r} met".format(r=req.mountpoint))
				# purge.append(req)

			# else:
				# print(req.mountpoint, mountpoint)

		# for p in purge:
			# required_mounts.remove(p)

	result = Measurement()
	good = 0
	for req in target.mounts:
		# logger.info("checking if " + req.mountpoint + " was found")
		name = "mount." + req.mountpoint.partition("/")[-1]
		if req.mountpoint in found_mounts:
			result.add_message(name, True)
			good += 1

		else:
			result.add_message(name, False)

	if good == len(target.mounts):
		result.state = "GOOD"

	else:
		result.state = "FAILED"

	return result

measure_server_ssh_mountpoints.label = "mounts"

def measure_server_ssh_sysinfo(target:Server, context:Context):
	"""Retreive system info as measurement messages.

	Reads:
	- OS
	- RAM / swap available / free
	- CPU count and total usage
	- net i/o
	- disk i/o
	"""
	raise NotImplementedError()

measure_server_ssh_sysinfo.label = "sysinfo"
