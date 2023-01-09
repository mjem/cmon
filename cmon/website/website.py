#!/usr/bin/env python3

"""Implementation of Website class."""

import logging
from typing import Iterable
from typing import Union

from ..testable import Testable
from ..server.server import ConnectionException

import httpx

logger = logging.getLogger("website")

class URL:
	"""A labelled URL string."""
	def __init__(self,
				 url:str,
				 label:str=None,
				 http_user:str=None,
				 http_password:str=None,
				 required:bool=True):
		self.url = url
		self.label = label
		self.http_user = http_user
		self.http_password = http_password
		self.required = required

	def __str__(self):
		return self.url

class Website(Testable):
	"""Representation of a website to be tested."""
	def __init__(self,
				 database:"Database"=None,
				 url:Iterable[Union[URL,str]]=None,
				 server:Iterable["Server"]=None,
				 http_user:str=None,
				 http_password:str=None,
				 label:str=None,
				 ):
		super().__init__(label=label)
		self.database = database
		self.url = url
		self.server = server
		self.http_user = http_user
		self.http_password = http_password

	def get(self, url):
		# data = {'username': username, 'password': password}
		params = None
		cookies = None
		auth = None

		if isinstance(url, URL):
			url = url.url

		try:
			response = httpx.get(url)
		except httpx.ConnectError as e:

			raise ConnectionException(request.url) from e

		return response

	def validate(self, response):
		"""Check `response` and return true if it looks good, otherwise an error string.

		Checks are:
		- server response code
		- non-zero data length
		- if HTML, check for obvious problems like write me
		(must be worse than just invalid HTML. Check for obvious server error messages)
		- I guess we could run it through a headless server and check for render or javascript
		errors
		"""
		if not httpx.codes.is_success(response.status_code):
			return "Bad code {cc} ({name})".format(cc=response.status_code,
												   name=httpx.codes(response.status_code))

		body = response.text
		logger.info("web test validate code {code} len {len}".format(
			code=response.status_code, len=len(body)))

		return True

	def links(self) -> Iterable[Testable]:
		if self.server is not None:
			return [self.server]

		else:
			return []
