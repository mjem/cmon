#!/usr/bin/env python3

def make_error_messages(results) -> Iterable[str]:
	"""Examine a set of results and yield a set of errors for any failed tests."""
	pass

def process_errors(results,
				   output_filename,
				   sendmail_receivers,
				   sendmail_sender,
				   sendmail_subject):
	"""Examine `results`, write an errors file if `output_filename`, and send emails.

	Emails requires a list of receivers in the format list of strings where each
	string is either a plain address or "Name <address@example.com>".
	Email sender if the same.
	Email subject is a jinja template expanded with context
	error_count
	"""
	pass

