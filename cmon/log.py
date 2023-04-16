#!/usr/bin/env python3

"""Initialise log system."""

import logging

def init_log(level:int=logging.DEBUG):
	logging.basicConfig(level=level)

