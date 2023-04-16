#!/usr/bin/env python3

"""Implementation of dataflow tests."""

from datetime import timedelta
from datetime import datetime
from fnmatch import fnmatch

# import humanize

from ..measurement import Measurement
from ..measurement import MeasurementState
from ..measurement import MessageDescription
from ..measurement import Message
from ..measurement import measure
from ..server.server import Server
from .dataflow import Dataflow
from ..context import Context

message_description_outage = MessageDescription(
	label="Dataflow outage",
	description="Show how long ago the dataflow was last active",
	datatype=timedelta,
	# quantisation=Nargs.MULTIPLE,
	# importance=Important.DASHBOARD,
	)

@measure(
	label="Dataflow outage",
	name="outage",
	description="Test if data if flowing with acceptable timeliness",
	subject_type=Dataflow,
	messages=[
		MessageDescription(
			name="files",
			label="Matching files",
			description="Number of files in dataflow directory matching our pattern",
			datatype=int),
		MessageDescription(
			name="newest",
			label="Newest file",
			description="Timestamp of most recent matching file",
			datatype=datetime)
	]
)
def measure_dataflow_outage(subject:Dataflow, context:Context):
	"""Test if the last modification to any file in a dataflow is older than threshold."""
	client = subject.server.ssh_connect()
	sftp = client.open_sftp()
	# sftp.chdir(target.directory)
	matches = 0
	latest = None
	age = None
	for fileattr in sftp.listdir_iter(subject.directory):
		if fnmatch(fileattr.filename, subject.pattern):
			matches += 1
			if latest is None or fileattr.st_mtime > latest:
				latest = fileattr.st_mtime

	result = Measurement()
	result.add_message(Message("files", matches))

	if matches == 0:
		result.state = MeasurementState.FAILED
		return result

	latest = datetime.utcfromtimestamp(latest)
	age = datetime.utcnow() - latest
	result.add_message(Message("newest", latest))
	if age < subject.max_outage:
		result.state = MeasurementState.GOOD

	else:
		result.state = MeasurementState.FAILED

	return result
