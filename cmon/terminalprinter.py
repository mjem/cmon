#!/usr/bin/env python3

"""Implementation of Printer class."""

from typing import Callable

import sys

INDENTATION = "  "
NEWLINE = "\n"
SECTION = ":"

class TerminalPrinter:
	def __init__(self, target=sys.stdout, indent=0, indentation=INDENTATION):
		self.target = target
		self.indent_level = indent
		self.indentation = indentation

	def write_line(self, line):
		"""Write a basic indented line."""
		self.target.write("{i}{line}{newline}".format(
			i=self.indentation * self.indent_level,
			line=line,
			newline=NEWLINE))

	def begin_section(self, section:str, postfix:str=None):
		"""Start a new section in the heirarchy.

		`section` gives the section name. `postfix` allows for text after the colon.
		"""
		self.write_line(section + SECTION + (" {postfix}".format(
			postfix=postfix) if postfix is not None else ""))
		self.indent()

	def end_section(self):
		"""End of section."""
		self.unindent()

	def label(self, name=None, label=None):
		"""Show an objects label if it has one, otherwise its name."""
		if label is not None:
			return " '{label}'".format(label=label)

		elif name is not None:
			return " '{label}'".format(label=name)

		else:
			return ""

	def docstring_single(self, obj:Callable) -> str:
		"""Pull out a bit of an objects docstring."""
		if obj.__doc__ is not None:
			docstring = obj.__doc__
			first_line, _, _ = docstring.partition(NEWLINE)
			while first_line.endswith("."):
				first_line = first_line[:-1]

			return first_line

		else:
			return obj.__name__

	def indent(self, amount=1):
		"""Increase indent level for subsequent writes."""
		self.indent_level += amount

	def unindent(self, amount=-1):
		"""Decrease indent level."""
		self.indent_level += amount
