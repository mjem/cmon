#!/usr/bin/env python3

"""Implementation of measurement classes."""

import logging
from enum import Enum
from typing import Iterable
from typing import Union
from typing import Callable
from typing import Dict
from datetime import datetime
from datetime import timedelta

from .testable import Testable

logger = logging.getLogger()

class MeasurementState(Enum):
	"""Overall result of a test."""
	GOOD = "good"
	NOT_APPLICABLE = "n/a"
	FAILED = "failed"
	ERROR = "error"
	MIXED = "mixed"
	IN_PROGRESS = "in progress"
	EMPTY = "empty"

MeasurementState.GOOD.description = "Measurement was made and was successful"
MeasurementState.NOT_APPLICABLE.description = "Measurement was skipped as not relevant"
MeasurementState.FAILED.description = "Measurement was made but a problem was detected"
MeasurementState.ERROR.description = "Measurement could not be reliably made due to an error"
MeasurementState.MIXED.description = "A mixure of good and bad results"
MeasurementState.IN_PROGRESS.description = "The result is being processed"

class MessageDescription:
	"""Additional information that forms part of a measurement result."""
	def __init__(self,
				 label:str,
				 name:str=None,
				 description:str=None,
				 # quantisation,  # choose between required, optional or multiple
				 # importance,  # choose between messages shown on the main dashboard
				 # and messages shown only on the tooltip
				 datatype:object=str,
				 unit:str=None,
				 display:str=None,
				 hidden:bool=False,
				 multiple:object=None):
		"""Args:
		- `label`: Visible brief label for this measurement messaage
		- `name`: An optional internal name used for database and file storage and to refer to the message
			in code
		- `description`: Long label for this message, used for example in mouse popups
		- `datatype`: Datatype (str, bool, int, float, datetime, timedelta, url) for the message
		- `unit`: Allow numerical types to specify a unit
		- `multiple`: Message is singular (None), optional (bool), a list (list) or named (dict)
		"""
		self.label = label
		self.name = name
		self.description = description
		self.datatype = datatype
		self.unit = unit
		self.display = display
		self.multiple = multiple

def measure(
		label:str,
		subject_type:type,
		name:str=None,
		description:str=None,
		messages:Iterable[MessageDescription]=[]):
	"""Decorator to declare a measurement used to test a subject."""
	def decorator_imp(func):
		def func_imp(*args, **kwargs):
			result = func(*args, **kwargs)
			return result

		func_imp.label = label
		func_imp.name = name
		func_imp.subject_type = subject_type
		func_imp.description = description
		func_imp.messages = messages
		func_imp.decorator = measure
		return func_imp

	return decorator_imp

class Message:
	"""Give additional context to a test result."""
	def __init__(self,
				 name:str,
				 value:Union[str, int, float, bool]=None,
				 parameter:str=None,
				 description:MessageDescription=None,
				 error:str=None):
		"""Args:
		- `name`: Message description name.
		- `value`: Contents of the message. Type must match the message description datatype.
		- `parameter`: Blank for a singlular message, ints for an array message, string key for a
			dict message
		- `description`: Link to the description object. The link is usually bound after the message
			has been created
		- `error`: There was a problem workng out this message. The error is always a string regardless
		lf the message datatype. The normal value is ignored
		"""
		self.name = name
		self.value = value
		self.parameter = parameter
		self.description = description
		self.error = error

	def __str__(self):
		if self.value is None:
			value = "n/a"

		elif isinstance(self.value, bool):
			value = "true" if self.value else "false"

		else:
			value = self.value

		return "{name}={value}".format(name=self.name, value=value)

class Measurement:
	"""The results returned by a single test against a single target.

	The main state attribute is used for a traffic lights display.
	The messages are a set of variable parameters, qualified.
	"""
	def __init__(self,
				 state:Union[MeasurementState,str]=MeasurementState.IN_PROGRESS,
				 subject:Union[Testable,Callable]=None,
				 messages:Iterable[Message]=None,
				 test_fn:callable=None,
				 ):
		"""Args:
		- `subject`: The thing we tested
		- `state`: Overall status of the subject of this measurement
		- `messages`: Additional text messages giving more data about tests of this subject
		- `children`: Additional results of components of our `subject`
		"""
		self.subject = subject
		self.state = state
		self.test_fn = test_fn
		if messages is None:
			self.messages = []

		else:
			self.messages = messages

	def get_state(self):
		return self._state

	def set_state(self, state:Union[MeasurementState,str]):
		if isinstance(state, str):
			self._state = MeasurementState[state]
			# logger.info("measurement set _state " + str(self._state) + " from " + state)

		else:
			self._state = state

	state = property(get_state, set_state)

	def __str__(self):
		if self.state is MeasurementState.GOOD:
			return "ok"

		else:
			return "nok: {message}".format(message=". ".join(str(s) for s in self.messages))

	def add_message(self,
					message:Message):
					# name:str,
					# value:Union[str, int, float, bool, datetime, timedelta],
					# description:MessageDescription=None):
		self.messages.append(message)
		# self.messages.append(Message(name=name, value=value, description=description))

	def add_child(self, child:"Measurement"):
		if self.children is None:
			self.children = []

		self.children.append(child)

	def traffic_lights(self):
		"""Set our state based on our childs state."""
		if self.children is None or len(self.children) == 0:
			self.state = MeasurementState.NOT_APPLICABLE
			return

		good_count = 0  # GOOD
		bad_count = 0  # either FAILED or ERROR
		for child in self.children:
			if child.state is MeasurementState.GOOD:
				good_count += 1

			elif child.state in (MeasurementState.FAILED, MeasurementState.ERROR):
				bad_count += 1

		if good_count == len(self.children):
			self.state = MeasurementState.GOOD

		elif bad_count == len(self.children):
			self.state = MeasurementState.FAILED

		else:
			self.state = MeasurementState.MIXED


# class TestRun:
# 	"""Store all the measurements from a run of the tests."""
# 	def __init__(self,
# 				 # top_subject:Testable,
# 				 top_measurement:Measurement,
# 				 simulate:bool,
# 				 verbose:bool):
# 		self.top_subject = top_subject
# 		self.simulate = simulate
# 		self.verbose = verbose
# 		self.execution_start = datetime.utcnow()
# 		# self.measurements = {}
# 		self.top_measurement = top_measurement

# 	def __getitem__(self, key):
# 		return self.measurements[key]

# 	def __setitem(self, key, value):
# 		self.measurements[key] = value

def traffic_light(results:Dict[Testable, MeasurementState],
				  subject:Testable,
				  new_state:MeasurementState) -> None:
	"""Set state of parent objects to reflect child results."""
	if new_state is MeasurementState.ERROR:
		results[subject] = MeasurementState.ERROR

	elif new_state is MeasurementState.GOOD:
		if results[subject] is MeasurementState.EMPTY:
			results[subject] = MeasurementState.GOOD

		elif results[subject] is MeasurementState.ERROR:
			results[subject] = MeasurementState.MIXED

	elif new_state is MeasurementState.FAILED:
		if results[subject] is MeasurementState.EMPTY:
			results[subject] = MeasurementState.FAILED

		elif results[subject] is MeasurementState.GOOD:
			results[subject] = MeasurementState.MIXED

