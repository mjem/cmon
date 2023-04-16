#!/usr/bin/env python3

import stat
from pathlib import Path
from invoke import task

# Location of project source code
# package_dir = Path("cmon")

# List of files to package
# source_files = [package_dir, "tasks.py"]

# Current dir
here = Path(__file__).parent

# Script to setup dev environment
activate_filename = here.joinpath("activate")

# Location fo virtual env
env_dir = here.joinpath("env")

def dev_activate(c):
	"""Make activate script to enable debug execution."""
	activate_filename.open("w").write("""#!/bin/bash
export PYTHONPATH={here}:$PYTHONPATH
{env_activate}export PATH={here}/bin:$PATH
eval "$({env_dir}/bin/register-python-argcomplete {here}/bin/cmon)"
""".format(
	here=here,
	env_activate="source {env}/bin/activate\n".format(env=env_dir) if env_dir.exists() else "",
	env_dir=env_dir))
	activate_filename.chmod(activate_filename.stat().st_mode | stat.S_IEXEC)
	print("Wrote {activate}".format(activate=activate_filename))

def dev_isort(c):
	"""Fix imports"""
	c.run("isort --sl {files}".format(files=" ".join(str(c) for c in source_files)))

def dev_lint_fix(c):
	"""run the tool to auto-lint code. (grey?, autopep8?, zapf?, not black)"""
	pass

def dev_3rdparty(c):
	"""Download and unpack 3rd party packages from source locations.

	(for development and upgrading 3rd party files only, as the files needed to
	actually run the tool are included in the normal repo and tarball)
	"""
	# Bootstrap
	# Download and unpack to 3rdparty
	# https://github.com/twbs/bootstrap/releases/download/v5.3.0-alpha1/bootstrap-5.3.0-alpha1-dist.zip
	# Bootstrap icons
	# https://github.com/twbs/icons/releases/download/v1.10.3/bootstrap-icons-1.10.3.zip
	pass

def dev_favicon(c):
	"""Convert favicon file from the boostrap-icons SVG into an ICO file."""
	# Requires inkscape, imagemagik available
	c.run("inkscape -w 64 -h 64 -o cmon.ico cmon/3rdparty/bootstrap-icons-1.10.3/speedometer.svg")
	c.run("convert cmon.png cmon/templates/cmon.ico")

def dev_license(c):
	"""Download (and convert?) the gpl3 license files as RST."""
	# https://www.gnu.org/licenses/gpl-3.0.rst
	pass

def dev_venv(c):
	"""Create venv with all packages to run, test and develop application."""
	c.run("python3 -m venv {env}".format(env=env_dir))
	c.run("{env}/bin/pip3 install --upgrade pip".format(env=env_dir))
	c.run("{env}/bin/pip3 install -r requirements.txt".format(env=env_dir))
	c.run("{env}/bin/pip3 install -r requirements-dev.txt".format(env=env_dir))

def dev_release(c):
	"""Prepare a release.

	- Run lint and autodoc reports
	- Run automated tests
	- Check everything is committed with no stray files
	- Check last commit has a valid tag
	- Update version file from git tag.
	- Build source tarball.
	- Push to upstream
	"""
	pass

@task(help={
	"activate": "Create activate file",
	"venv": "Create virtual environment"
	# "fix": "Run code fix tools: yapf? autopep8? isort-fix? grey? something else?"
	# "release": "Run tests, build docs, stamp version number, make release tarball, check repo is clean",
	# "license": "Rebuild license file (GPL-3)",
	# "thirdparty": "Download and unpack 3rd party files modules",
	})
def dev(c,
		activate=False,
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
	# - Unfortunately the various checkers don't have flexible enough output options to
	# allow them all to be configured to output in a consistent way
	# - pylint gives good results but doesn't seem to work well with pyproject.toml
	# or setup.cfg so we use .pylintrc
	c.run("pylint {files}".format(files=" ".join(str(c) for c in source_files)))
	# - pycodestyle gives good results. Use setup.cfg for configuration because it doesn't
	# read from pyproject.toml properly yet
	c.run("pycodestyle {files}".format(files=" ".join(str(c) for c in source_files)))
	# - pydocstyle gives good results. Configuration?
	c.run("pydocstyle {files}".format(files=" ".join(str(c) for c in source_files)))
	# - mypy fails to read "no_implicit-optional=False" from either .mypy.ini
	# or pyproject.toml
	# mypy disabled as it's not happy with the flexible argument style used by many of the Testable
	# classes
	# c.run("mypy --implicit-optional {files}".format(files=" ".join(str(c) for c in source_files)))
	# one line per import
	# - isort gives good results on import ordering
	c.run("isort --check --sl {files}".format(files=" ".join(str(c) for c in source_files)))
	# - mccabe doesn't appear to be functional with this project
	# c.run("python3 -m mccabe --min 5 {files}".format(files=" ".join(str(c) for c in source_files)))
	# - vale or similar spelling/grammar checker would be nice if there was one that can easily
	# be configured to test docstrings, comments and RST files
	# - Should try setting up html/js/css validators, especially if someone ever writes one
	# that can handle multilanguage source files like css/js inside html, html jinja2 templates,
	# or html/css/js inside python source files
	# - gitlint to check repo state?
	# - filelint for generic file checks?
	# - org lint?

@task
def doc(c):
	"""Build automatic documentation."""
	# - Process embedded code in README.org converting to README.rst
	c.run("pandoc README.org -o README.rst")
	# - Create combined sphinx source site including README, extra manual pages,
	# lint results, autotest results
	# - Build html and pdf documents
	# c.run("pandoc README.org --css pandoc.css -o README.rst")
	# css option doesn't work when converting org to html

@task
def test(c,
		 start=False,
		 run=False,
		 stop=False):
	"""Run automated tests."""
	# - start/stop docker containers
	# - pytest of files in tests/ directory
	# - doctest of tests in docstrings
	if start:
		# https://github.com/schollm/docker-composer
		# use composer module instead
		c.run("docker-compose -f tests/docker-compose.yaml up -d")

	if stop:
		# use composer module instead
		c.run("docker rm -f cmon_website cmon_sshserver cmon_database")

	if run:
		# import pytest
		# pytest.?
		raise NotImplementedError()
