#!/usr/bin/env python3

"""Measurement tests to be run against websites."""

import logging

from ..utils import is_listlike
from ..context import Context
from .website import Website
from ..measurement import Measurement

logger = logging.getLogger("webtests")

def measure_web_urls(target:Website, context:Context):
	# logger.info("Retrieving from {url}".format(url=target.url))
	if is_listlike(target.url):
		use_urls = target.url

	else:
		use_urls = [target.url]

	result = Measurement("GOOD")
	for use_url in use_urls:
		response = target.get(use_url)
		check = target.validate(response)
		if check is not True:
			result.state = "FAILED"
			result.add_message(use_url, check)

	return result