CMON
====

Introduction
------------

`cmon` is a tool for testing and documenting a system of servers and services.

You edit a configuration file to describe the system, then run `cmon` to either run automated
tests to report on how well the system is running, or output a system diagram.

Quickstart
----------

`cmon` needs a configuration file describing a network of servers and other objects
in order to work.
Either write one based on a local system (see configuration file docs)
or use the sample configuration file and start up a system of docker containers
to create the system

The local network requires ports 21000-21002 to be available. Edit `docker/Dockerfile`,
`conf/sample_config.py` to change this.

# Grab the source code
https://github.com/mjem/cmon.git
# Set up virtual environment
python3 -m venv env
# Activate virtual env and application
. env/bin/activate
# Display sample configuration file
cmon --config-py sample/sample_config.py --show-config
# Set up sample network of web server, postgres server and a dummy logging application
docker-compose -f sample/docker-compose.yaml up -d
# Display test results to console
cmon --config-py conf/example_config.py --output-console
# Make website of test results
cmon --config-py conf/example_config.py --output-web output
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
- Sample configuration file and system not implemented
- No support for Oracle or sqlite3 databases

Copyright
---------

This project is copyright (C) 2023 Mike Elson
