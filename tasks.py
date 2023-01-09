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
