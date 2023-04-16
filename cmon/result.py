#!/usr/bin/env python3

"""Handling of measurement test result objects."""

from .terminalprinter import TerminalPrinter
from .measurement import Measurement

def markup(in_str:str) -> str:
	"""Make `in_str` safe for writing to dot delimited files.

	If the input string contains spaces or dots, the output will have quotes around it.
	If it's given quotes and also contains quotes they are prefixed with a backslash.
	Backslashes in the input are doubled up.
	"""
	res = str(in_str)

	if "." in res:
	# if isinstance(in_str, str) and "." in in_str:
		return "\"{s}\"".format(s=res)

	return res


def result_lines(output:TerminalPrinter,
				 measurement:Measurement) -> None:
	"""Take a single measurement and messages and write to database friendly lines.

	Format of each line is

	(for the overall result)
	classname.objectname.testname=traffic light result
	(per singlular message)
	classname.objectname.testname.messagename=value
	(message array)
	classname.objectname.testname.messagename.0=value
	(parameterised or dict messages)
	classname.objectname.testname.messagename.parameter=value
	"""
	# print("write measurement", measurement, "subject", measurement.subject,
		  # "subject label", measurement.subject.label, "subject name", measurement.subject.name)
	output.write_line("{classname}.{objectid}.{testname}={result}".format(
		classname=markup(type(measurement.subject).name),
		objectid=markup(measurement.subject.get_id()),
		testname=markup(measurement.test_fn.name),
		result=measurement.state.name))
	for message in measurement.messages:
		# print("message", message, "description", message.description)
		if message.error is None:
			output.write_line(
				"{classname}.{objectid}.{testname}.{messagename}{parameter}={value}".format(
					classname=markup(type(measurement.subject).name),
					objectid=markup(measurement.subject.get_id()),
					testname=markup(measurement.test_fn.name),
					messagename=message.name,
					parameter="" if message.parameter is None else ".{param}".format(
						param=message.parameter),
					value=markup(message.value)))

		else:
			output.write_line(
				"{classname}.{objectid}.{testname}.{messagename}{parameter}=ERROR: {error}".format(
					classname=markup(type(measurement.subject).name),
					objectid=markup(measurement.subject.get_id()),
					testname=markup(measurement.test_fn.name),
					messagename=message.name,
					parameter="" if message.parameter is None else ".{param}".format(
						param=message.parameter),
					error=message.error))
