#!/usr/bin/env python3

"""Miscellaneous helper functions."""

import collections

def is_listlike(obj):
	"""Does `obj` look like an iterable list?"""
	return isinstance(obj, collections.abc.Sequence) and \
		not isinstance(obj, (str, collections.abc.ByteString))
