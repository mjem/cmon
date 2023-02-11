#!/usr/bin/env python3

import stat
from pathlib import Path
from invoke import task

package_dir = Path("cmon")
source_files = [package_dir, "tasks.py"]

here = Path(__file__).parent
activate_filename = Path("activate")

def dev_activate(c):
	"""Make activate script."""
	activate_filename.open("w").write("""#!/bin/bash
export PYTHONPATH={here}:$PYTHONPATH
{env}export PATH={here}/bin:$PATH
""".format(here=here, env="source {here}/env/bin/activate\n".format(here=here) if here.joinpath("env").exists() else ""))
	activate_filename.chmod(activate_filename.stat().st_mode | stat.S_IEXEC)
	print("Wrote {activate}".format(activate=activate_filename))

def dev_isort(c):
	"""Fix imports"""
	c.run("isort --sl {files}".format(files=" ".join(str(c) for c in source_files)))

def dev_lint_fix(c):
	"""run the tool to auto-lint code. (black(!), grey, autopep8, zapf)"""
	pass

def dev_3rdparty(c):
	"""Download and unpack 3rd party packages from source.

	(This is for development and upgrading 3rd party files as the files needed to
	run the tool are included in the normal archive.)
	"""
	# Bootstrap
	# Download and unpack to 3rdparty
	# https://github.com/twbs/bootstrap/releases/download/v5.3.0-alpha1/bootstrap-5.3.0-alpha1-dist.zip
	# Bootstrap icons
	# https://github.com/twbs/icons/releases/download/v1.10.3/bootstrap-icons-1.10.3.zip
	pass

def dev_favicon(c):
	"""Convert favicon file."""
	c.run("inkscape -w 64 -h 64 -o cmon.ico cmon/3rdparty/bootstrap-icons-1.10.3/speedometer.svg")
	c.run("convert cmon.png cmon/templates/cmon.ico")

def dev_license(c):
	"""download and convert the gpl3 license files."""
	# https://www.gnu.org/licenses/gpl-3.0.rst
	pass

def dev_venv(c):
	"""Create venv with all packages to run, test and develop application."""
	c.run("python3 -m venv env")
	c.run("env/bin/pip3 install --upgrade pip")
	c.run("env/bin/pip3 install -r requirements.txt")
	c.run("env/bin/pip3 install -r requirements-dev.txt")

def dev_release(c):
	"""Prepare a release.

	Update version from git tag.
	Make source package.
	"""
	pass

@task(help={
	"activate": "Create activate file",
	"venv": "Create virtual environmentin 'env' directory"
	# "fix": "Run code fix tools: yapf? autopep8? isort-fix? grey? something else?"
	# "release": "Run tests, build docs, stamp version number, make release tarball, check repo is clean",
	# "license": "Rebuild license file (GPL-3)",
	# "thirdparty": "Download and unpack 3rd party files modules",
	})
def dev(c,
		activate=True,
		venv=False,
		# fix=False,
		# release=False,
		# license=False,
		# thirdparty=False
		):
	"""Development options."""
	if venv:
		dev_venv(c)

	if activate:
		dev_activate(c)

	# dev_thirdparty()
	# dev_license()
	# dev_favicon()


@task
def lint(c):
	"""Run static code checkers."""
	c.run("pylint {files}".format(files=" ".join(str(c) for c in source_files)))
	c.run("pycodestyle {files}".format(files=" ".join(str(c) for c in source_files)))
	c.run("pydocstyle {files}".format(files=" ".join(str(c) for c in source_files)))
	# mypy fails to read "no_implicit-optional=False" from either .mypy.ini
	# or pyproject.toml
	# mypy disabled as it's not happy with the flexible argument style used by many of the Testable
	# classes
	# c.run("mypy --implicit-optional {files}".format(files=" ".join(str(c) for c in source_files)))
	# one line per import
	c.run("isort --check --sl {files}".format(files=" ".join(str(c) for c in source_files)))
	# doesn't appear to be functional
	# c.run("python3 -m mccabe --min 5 {files}".format(files=" ".join(str(c) for c in source_files)))
	# language tests: vale?
	# html/js/css tests: htmlvalidate?
	# gitlint?
	# filelint?

@task
def doc(c):
	"""Build automatic documentation."""
	pass

@task
def build(c):
	"""Build and release options."""
	# make tarball
	# prepare release - read git tag and put into versions file, run checks and generate docs
	pass

@task
def install(c):
	"""Install software to another location."""
	pass
