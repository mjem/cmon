#!/usr/bin/env python3

from pathlib import Path
from invoke import task

package_dir = Path("cmon")
source_files = [package_dir, "tasks.py"]

def dev_activate(c):
	"""Make activate script."""
	pass

def dev_isort(c):
	"""Fix imports"""
	c.run("isort --sl {files}".format(files=" ".join(str(c) for c in source_files)))

def dev_lint_fix(c):
	"""run the tool to auto-lint code. (black(!), grey, autopep8, zapf)"""
	pass

def dev_3rdparty(c):
	"""Download and unpack all 3rd party packages from source.

	(This is for development and upgrading 3rd party files as the files needed to
	run the tool are included in the normal archive.)
	"""
	# Bootstrap
	# Download and unpack to 3rdparty
	# https://github.com/twbs/bootstrap/releases/download/v5.3.0-alpha1/bootstrap-5.3.0-alpha1-dist.zip
	# Bootstrap icons
	# https://github.com/twbs/icons/releases/download/v1.10.3/bootstrap-icons-1.10.3.zip
	pass

def dev_license(c):
	"""download and convert the gpl3 license files."""
	# https://www.gnu.org/licenses/gpl-3.0.rst
	pass

def dev_env(c):
	"""Create venv with all packages to run, test and develop application."""
	pass

def dev_release(c):
	"""Prepare a release.

	Update version from git tag.
	Make source package.
	"""
	pass

@task
# --activate -> make activate file
# --venv -> make virtual env
# --fix -> yapf/autopep8, isort-fix
# --release -> run tests, make docs, stamp version info into project files, make release tarball
# --license -> rebuild license file
# --3rdparty -> re-download 3rd party files except license (normalise, reset, jquery, bootstrap)
def dev(c):
	"""Create activate file."""
	#
	pass

@task
def lint(c):
	"""Static code checkers."""
	c.run("pylint {files}".format(files=" ".join(str(c) for c in source_files)))
	c.run("pycodestyle {files}".format(files=" ".join(str(c) for c in source_files)))
	c.run("pydocstyle {files}".format(files=" ".join(str(c) for c in source_files)))
	# mypy fails to read "no_implicit-optional=False" from either .mypy.ini
	# or pyproject.toml
	c.run("mypy --implicit-optional {files}".format(files=" ".join(str(c) for c in source_files)))
	# one line per import
	c.run("isort --check --sl {files}".format(files=" ".join(str(c) for c in source_files)))
	c.run("python3 -m mccabe --min 5 {files}".format(files=" ".join(str(c) for c in source_files)))
	# language
	# html/js/css
	# check project files
	# gitlint
	# filelint

@task
def lint(c):
	pass

@task
def doc(c):
	pass
