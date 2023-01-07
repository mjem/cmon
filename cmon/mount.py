#!/usr/bin/env python3

"""Implementation of Mount class."""

class Mount:
	"""Representation of a mountpoint."""
	def __init__(self,
				 mountpoint:str,
				 label:str=None,
				 required=True):
		self.mountpoint = mountpoint
		self.label = label
		self.required = required
