#!/usr/bin/env python3

"""Implementation of dataflow tests."""

from datetime import timedelta
from datetime import datetime
from fnmatch import fnmatch

import humanize

from ..measurement import Measurement
from ..measurement import MeasurementState
from ..measurement import MessageDescription
from ..server.server import Server
from ..context import Context

message_description_outage = MessageDescription(
	label="Dataflow outage",
	description="Show how long ago the dataflow was last active",
	datatype=timedelta,
	# quantisation=Nargs.MULTIPLE,
	# importance=Important.DASHBOARD,
	)

def measure_dataflow_outage(target:Server, context:Context):
	"""Test if the last modification to any file in a dataflow is older than threshold."""
	client = target.server.ssh_connect()
	sftp = client.open_sftp()
	# sftp.chdir(target.directory)
	matches = 0
	latest = None
	age = None
	for fileattr in sftp.listdir_iter(target.directory):
		if fnmatch(fileattr.filename, target.pattern):
			matches += 1
			if latest is None or fileattr.st_mtime > latest:
				latest = fileattr.st_mtime

	result = Measurement()
	result.add_message("matching files", matches)

	if matches == 0:
		result.state = MeasurementState.FAILED
		return result

	latest = datetime.utcfromtimestamp(latest)
	age = datetime.utcnow() - latest
	result.add_message("newest", latest)
	result.add_message("age", age)
	if age < target.max_outage:
		result.state = MeasurementState.GOOD

	else:
		result.state = MeasurementState.FAILED

	return result

measure_dataflow_outage.label = "outage"
