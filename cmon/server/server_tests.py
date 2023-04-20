#!/usr/bin/env python3

"""Implementation of tests against a server."""

import time
import logging
from copy import copy

import humanize

from ..measurement import Measurement
from ..measurement import measure
from ..measurement import MeasurementState
from ..measurement import MessageDescription
from ..measurement import Message
from .server import Server
from .server import ConnectionException
from ..context import Context
from ..shell import shell
from ..shell import shell_validate
from .df import decode_df
from ..utils import is_listlike

logger = logging.getLogger()

NEWLINE = "\n"

@measure(
	label="Ping",
	name="ping",
	description=("Check we can ping the server. Failed only indicates a lack of ICMP response "
				 "and does not mean the server itself is down"),
	subject_type=Server,
	messages=[
		MessageDescription(
			name="ip",
			label="Response time",
			description="Response time per address",
			unit="ms",
			sf=4,
			datatype=float,
			multiple=dict)
	]
)
def measure_server_ping(subject:Server, context:Context):
	"""Check the server responds to ping.

	Requires a response to an ICMP packet and failure to ping doesn't
	necessarily mean the server is down."""
	# if len(subject.ssh_config) > 0 or len(subject.ssh_user) > 0:
		# print(subject.ssh_config)
		# print(subject.ssh_user)
		# 1/0
		# return Measurement(state=MeasurementState.NOT_APPLICABLE)

	if context.simulate:
		logger.info("Simulating a ping of {s}".format(s=target))
		return

	start_time = time.time()
	shelled = shell("ping -c 1 " + subject.hostname)
	duration = time.time() - start_time
	# result = shell("ping -c 1 " + subject.hostname, verbose=True, echo=True)
	# logger.info("Ping status code {c}".format(c=result.returncode))
	valid = shell_validate(shelled)
	# logger.info("Successful ping of " + subject.hostname)
	if context.verbose:
		logger.info(shelled.stdout)

	if valid is True:
		result = Measurement(state=MeasurementState.GOOD,
							 messages=[
								 Message(name="ip",
										 parameter=subject.hostname,
										 # seconds to ms with 1 d.p.
										 value=duration*1000)])
		# result.add_message("host", subject.hostname)
		return result

	result = Measurement(state="FAILED")
	result.add_message(Message(name="ip",
							   parameter=subject.hostname,
							   error="ping command failed"))
	return result


@measure(
	label="SSH aliveness",
	name="ssh",
	description="Check we can ssh into the server",
	subject_type=Server,
	messages=[
		MessageDescription(
			name="user",
			label="User",
			description="SSH username",
			datatype=str)
	]
)
def measure_server_ssh_aliveness(subject:Server, context:Context):
	try:
		client = subject.ssh_connect()
		if client is None:
			return Measurement(state=MeasurementState.NOT_APPLICABLE)

	except ConnectionException as e:
		return Measurement(state=MeasurementState.FAILED, message=str(e))

	result = Measurement(state=MeasurementState.GOOD)
	if subject.ssh_user is not None:
		if is_listlike(subject.ssh_user):
			result.add_message(Message("user", subject.ssh_user[0]))

		else:
			result.add_message(Message("user", subject.ssh_user))

	return result


@measure(
	label="Mounts",
	name="mount",
	description="Check all configured mountpoints have a partition mounted",
	subject_type=Server,
	messages=[
		MessageDescription(
			name="size",
			label="Capacity",
			description="Total size of partition",
			unit="bytes",
			# humanize=True,  # display=MessageDisplay.BYTE_SIZE,
			template="{{parameter}}: {{used|filesizeformat}} used of {{value|filesizeformat}}",
			datatype=int,
			multiple=dict),
		MessageDescription(
			name="used",
			label="Used",
			description="Space used in partition",
			# unit="bytes",
			# humanize=True,  # show_disk_usage("size"),
			hidden=True,
			datatype=int,
			multiple=dict)
	]
)
def measure_server_ssh_mountpoints(subject:Server, context:Context) -> Measurement:
	"""Check all configured mountpoints are mounted."""
	if subject.mounts is None:
		return Measurement("NOT_APPLICABLE")

	client = subject.ssh_connect()
	if client is None:
		return Measurement(state=MeasurementState.FAILED, message=str(e))

	stdin, stdout, stderr = client.exec_command("df")
	error = stderr.read().decode().strip()

	# Use helper to decode actual df output
	found_mounts = decode_df(stdout.read().decode().split(NEWLINE))

	result = Measurement()
	good = 0
	# For each mount we are configured to look for
	for req in subject.mounts:
		# logger.info("checking if " + req.mountpoint + " was found")
		found_mount = found_mounts.get(req.mountpoint)
		if found_mount:
			result.add_message(Message(name="size", value=found_mount.total, parameter=req.mountpoint))
			result.add_message(Message(name="used", value=found_mount.used, parameter=req.mountpoint))
			good += 1

		else:
			result.add_message(Message(name="size", error="not mounted", parameter=req.mountpoint))
			result.add_message(Message(name="used", error="not mounted", parameter=req.mountpoint))

	if good == len(subject.mounts):
		result.state = "GOOD"

	else:
		result.state = "FAILED"

	return result

@measure(
	label="System info",
	name="sysinfo",
	description="Show system information",
	subject_type=Server,
	messages=[
		MessageDescription(
			name="os",
			label="OS",
			description="Operating system"),
		MessageDescription(
			name="cpu",
			label="CPU count",
			description="Number of CPU cores",
			datatype=int),
		MessageDescription(
			name="memtotal",
			label="Total memory",
			description="Amount of memory installed on the server",
			datatype=int,
			unit="bytes",
			humanize=True,
			hidden=True),
		MessageDescription(
			name="memfree",
			label="Free memory",
			description="Amount of unused memory on the server",
			datatype=int,
			unit="bytes",
			humanize=True,
			template="RAM: {{value|filesizeformat}} free of {{memtotal|filesizeformat}}"
		),
	]
)
def measure_server_ssh_sysinfo(subject:Server, context:Context):
	"""Retreive system info as measurement messages.

	Reads:
	- OS
	- RAM / swap available / free
	- CPU count and total usage
	- net i/o
	- disk i/o
	"""
	logger.debug("Server sysinfo for {name}".format(name=subject))
	client = subject.ssh_connect()
	if client is None:
		return Measurement(MeasurementState.NOT_APPLICABLE)

	# Find OS from /etc/os-release file
	sftp = client.open_sftp()
	handle = sftp.open("/etc/os-release")
	result = Measurement(MeasurementState.GOOD)
	for line in handle.read().decode().split(NEWLINE):
		if len(line) == 0 or "=" not in line:
			continue

		key, _, value = line.partition("=")
		# print("len",len(line),"key",key,"value",value)
		if key == "PRETTY_NAME":
			result.add_message(Message("os", value.strip("\"")))

	# CPU
	stdin, stdout, stderr = client.exec_command("lscpu")
	for line in stdout.read().decode().split(NEWLINE):
		key, _, value = line.partition(":")
		value = value.lstrip(" ")
		# print("lscpu key",key,"value",value)
		if key == "CPU(s)":
			result.add_message(Message("cpu", value))

	# Memory
	stdin, stdout, stderr = client.exec_command("free")
	for line in stdout.read().decode().split(NEWLINE):
		# print("cells", line.split())
		cells = line.split()
		if len(cells) == 0:
			continue

		if cells[0] == "Mem:":
			result.add_message(Message("memtotal", cells[1]))
			result.add_message(Message("memfree", cells[2]))

	return result


# server.myserver.docker.image.containername=imagename
# server.myserver.docker.uptime.containername=uptime

# Server myserver:
#  Docker:
#   - mycontainer (myimage) uptime 3 days

@measure(
	label="Docker",
	name="docker",
	description="Report on running docker containers",
	subject_type=Server,
	messages=[
		MessageDescription(
			name="image",
			label="Docker image",
			description="Name of docker image used by container",
			multiple=dict,
			template="{{parameter}} ({{value}}) uptime {{uptime}}"
		),
		MessageDescription(
			name="uptime",
			label="Docker runtime",
			description="Time docker container has been running for",
			multiple=dict,
			datatype=str,  # timedelta,
			hidden=True),
	]
)
def measure_server_ssh_docker(subject:Server, context:Context):
	"""Retrieve information about running docker containers.

	Uses primary ssh connection and docker command line tool."""
	# Check we have ssh connections configured
	if subject.docker_containers is None:
		return Measurement(MeasurementState.NOT_APPLICABLE)

	# If ssh connection is not available for some reason then skip
	client = subject.ssh_connect()
	if client is None:
		return Measurement(MeasurementState.NOT_APPLICABLE)

	result = Measurement(MeasurementState.GOOD)
	stdin, stdout, stderr = client.exec_command(
		"docker ps --format \"{{.Names}},{{.Image}},{{.RunningFor}}\"")

	for line in stdout.read().decode().split(NEWLINE):
		if len(line) == 0:
			continue

		container_name, image_name, age = line.split(",")
		if image_name.startswith("harbor.opscloud.eumetsat.int/"):
			image_name = image_name[len("harbor.opscloud.eumetsat.int/"):]

		if age.endswith(" ago"):
			age = age[:-len(" ago")]

		result.add_message(Message("image", image_name, parameter=container_name))
		result.add_message(Message("uptime", age, parameter=container_name))

	return result
