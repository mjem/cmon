#!/usr/bin/env python3

"""Implementation of Measurement class."""

import logging
from enum import Enum
from typing import Iterable
from typing import Union

logger = logging.getLogger()

class MeasurementState(Enum):
	GOOD = "good"
	NOT_APPLICABLE = "n/a"
	FAILED = "failed"
	ERROR = "error"

MeasurementState.GOOD.description = "Measurement was made and was successful"
MeasurementState.NOT_APPLICABLE.description = "Measurement was skipped as not relevant"
MeasurementState.FAILED.description = "Measurement was made but a problem was detected"
MeasurementState.ERROR.description = "Measurement could not be made due to an error"

class MeasurementMessage:
	"""Variable result to give more info than simple pass/fail/n/a for a test."""
	def __init__(self,
				 name:str,
				 value:Union[str, int, float, bool]):
		self.name = name
		self.value = value

	def __str__(self):
		if self.value is None:
			value = "n/a"

		elif isinstance(self.value, bool):
			value = "true" if self.value else "false"

		else:
			value = self.value

		return "{name}={value}".format(name=self.name, value=value)

class MeasurementDescription:
	"""Only used by Test / Measurement objects to give meta info about their measurements."""
	def __init__(self,
				 label:str=None,
				 optional:bool=True,
				 datatype:object=str):
		pass

class Measurement:
	"""The results returned by a single test against a single target.

	The main state attribute is used for a traffic lights display.
	The messages are a set of variable parameters, qualified.
	"""
	def __init__(self,
				 state=None,
				 messages:Iterable[MeasurementMessage]=None):
		if messages is None:
			self.messages = []

		else:
			self.messages = messages

		self.state = state

	def get_state(self):
		return self._state

	def set_state(self, state):
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

	def add_message(self, name, value):
		self.messages.append(MeasurementMessage(name=name, value=value))
