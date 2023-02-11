Configuration file
==================

The `cmon` is configured with a Python file containing objects as described below.

Sample config
-------------

See `conf/sample_config.py` for an example configuration.
This file can be used along with `tests/start.sh` which creates a local
network of `docker` containers which create the network tested in the sample file.

Template
--------

See `conf/template_config.py` for a basic configuration file.

Dashboards
----------

The main configuration object holding a list of dashboards.

Dashboard
---------

A dashboard collects together a list of test suites and summarises them into a
single traffic light (green, yellow, red) result.

Test suite
----------

List of testables and list of tests.
The test suite generates a traffic light output for each testable, and combines them
into a status for the test suite.

Testables
---------

Testable is a base with the following derived classes:

Website
~~~~~~~

Representation of a database. The tool tests configured URLs against the website.

Backend
~~~~~~~

Backend is a fairly generic class for testing software on a server. The class
allows various tests to be configured against is.
The backend itself is an installation of software which may use a database,
server processes, docker containers and create log files.

Dataflow
~~~~~~~~

A directory or heirarchy of directories where files are reguarly created or updated.
`cmon` can be configured to check a dataflow for regular writes.

Database
~~~~~~~~

A database hosted on a server.

Server
~~~~~~

Representation of a server.

Tests
-----

A `test` is a simple Python function with the signature:

```
def fn(target:Server, context:Context) -> Measurement:
    pass

fn.label = "label"
```
