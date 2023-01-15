CMON
====

Introduction
------------

This is a tool for testing and documenting a system of servers and services.
The user describes a network of objects in a configuration file then uses the CMON tool to
either run automated tests against them, or can create a system diagram.

Quickstart
----------

CMON needs a configuration file describing a network of servers and other objects
in order to work.
Either write one based on a local system (see configuration file docs)
or use the sample configuration file and start up a system of docker containers
to create the system

# Grab the source code
https://github.com/mjem/cmon.git
# Set up virtual environment
python3 -m venv env
. env/bin/activate
# Install cmon and dependancies
pip3 install .
# Display sample configuration file
cmon --config-py conf/wald_config.py --show-config
# Set up sample network of postgres and web servers
<<<write me with docker. needs docker daemon running>>>
# Display test results to console
cmon --config-py conf/wald_config.py --output-console
# Make website of test results
cmon --config-py conf/wald_config.py --output-web output
# Open in a browser
firefox output.index.html

Configuration file options
--------------------------

See sample in `docs` for an example configuration file.

Project status
--------------

Incomplete. Main missing areas are:

- No option to write config file in YAML with a schema
- Server objects sysinfo test if not written
- Database tests are limited
- Backend tests are limited
- No authentication options for website tests
- Generated website is missing Design, Source and Options pages,
  and dynamic display of links between subjects and complete tooltips
- System design plantuml option not implemented
- Project tools (autodocs, autotests, lint) mostly not implements
- No options for secure password handling for databases
- Server objects cannot use ssh configuration file sections

Copyright
---------

This project is copyright (C) 2023 Mike Elson
