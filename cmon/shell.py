#!/usr/bin/env python3

import logging
import subprocess

logger = logging.getLogger()

def shell(cmd:str,
		  verbose=False,
		  echo=False,
		  capture_stdout=False) -> subprocess.CompletedProcess:
	if verbose:
		logger.info("Cmd: {cmd}".format(cmd=cmd))

	# capture_output = False
	# if echo or capture_stdout:
	capture_output = True

	cmd_split = cmd.split(" ")
	result = subprocess.run(cmd_split, capture_output=capture_output)
	if echo:
		logger.info(result.stdout)

	return result

def shell_validate(result):
	"""Examine a `result` from `shell()`. Return True if all good otherwise an error string."""
	try:
		result.check_returncode()
	except subprocess.CalledProcessError as e:
		return str(e)

	return True
