#!/usr/bin/env python3

"""Auto test using sample configuration file.

We create some docker containers running services (so the docker daemon must be running
and avaiable to the current user, then test them using sample config file,
generating a website output.
"""

def setup():
	"""Spin up postgres ad web servers in docker containers for sample config to use."""
	pass

def test_system_diagram():
	"""Make system diagram."""
	pass

def test_console():
	"""Run tests console output."""
	pass

def test_website():
	"""Build results website from sample config."""
	pass
