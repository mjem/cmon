#!/usr/bin/env python3

"""Measurement tests to be run against websites."""

import logging

from ..utils import is_listlike
from ..context import Context
from .website import Website
from ..measurement import Measurement
from ..measurement import MeasurementState
from ..measurement import Message
from ..measurement import measure
from ..measurement import MessageDescription

logger = logging.getLogger("webtests")

@measure(
	label="Web requests",
	name="web",
	description="Retrieve URLs from webserver",
	subject_type=Website,
	messages=[
		MessageDescription(
			name="response",
			label="Response time",
			description="Check timing, error code and non-empty response",
			unit="ms",
			sf=4,
			multiple=dict,
			datatype=float)
	]
)
def measure_web_urls(subject:Website, context:Context):
	# logger.info("Retrieving from {url}".format(url=target.url))
	result = Measurement(MeasurementState.GOOD)
	for url in subject.urls:
		response = subject.get(url)
		check = subject.validate(response)
		if check is True:
			if isinstance(url, str):
				display_url = url

			else:
				display_url = str(url)

			if display_url.endswith("/"):
				display_url = display_url[:-1]

			result.add_message(Message("response",
									   response.elapsed.total_seconds() * 1000,
									   parameter=display_url))

		else:
			result.add_message(Message("response",
									   error="Request failed",
									   parameter=url))
			result.state = MeasurementState.FAILED

	return result
