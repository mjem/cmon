#!/usr/bin/env python3

"""Implementation of measurement classes."""

import logging
from enum import Enum
from typing import Iterable
from typing import Union
from typing import Callable

from .testable import Testable

logger = logging.getLogger()

class MeasurementState(Enum):
	GOOD = "good"
	NOT_APPLICABLE = "n/a"
	FAILED = "failed"
	ERROR = "error"
	MIXED = "mixed"
	IN_PROGRESS = "in progress"

MeasurementState.GOOD.description = "Measurement was made and was successful"
MeasurementState.NOT_APPLICABLE.description = "Measurement was skipped as not relevant"
MeasurementState.FAILED.description = "Measurement was made but a problem was detected"
MeasurementState.ERROR.description = "Measurement could not be reliably made due to an error"
MeasurementState.MIXED.description = "A mixure of good and bad results"
MeasurementState.IN_PROGRESS.description = "The result is being processed"

class MessageDescription:
	"""Metadata about a measurement message."""
	def __init__(self,
				 label:str=None,
				 description:str=None,
				 # quantisation,  # choose between required, optional or multiple
				 # importance,  # choose between messages shown on the main dashboard
				 # and messages shown only on the tooltip
				 datatype:object=str,
				 unit:str=None):
		"""Args:
		- `label`: Quick label for this measurement messaage
		- `description`: Long label for this message
		- `datatype`: Datatype (str, bool, int or float) for the message
		- `unit`: Allow numerical types to specify a unit
		"""
		self.label = label
		self.description = description
		self.datatype = datatype
		self.unit = unit

class Message:
	"""Give additional context to a test result."""
	def __init__(self,
				 name:str,
				 value:Union[str, int, float, bool],
				 description:MessageDescription=None):
		self.name = name
		self.value = value
		self.description = description

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
				 children:Iterable["Measurement"]=None):
		"""Args:
		- `subject`: The thing we tested
		- `state`: Overall status of the subject of this measurement
		- `messages`: Additional text messages giving more data about tests of this subject
		- `children`: Additional results of components of our `subject`
		"""
		self.subject = subject
		self.state = state
		if messages is None:
			self.messages = []

		else:
			self.messages = messages

		if children is None:
			self.children = []

		else:
			self.children = children


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
					name:str,
					value:Union[str, int, float, bool],
					description:MessageDescription=None):
		self.messages.append(Message(name=name, value=value, description=description))

	def add_child(self, child:"Measurement"):
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
