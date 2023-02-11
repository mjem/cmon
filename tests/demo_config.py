#!/usr/bin/env python3

"""Sample cmon configuration file."""

import os
from pathlib import Path
from datetime import timedelta

from cmon.server.server import Server
from cmon.mount import Mount
from cmon.dashboards import Dashboards
from cmon.database.database import Database
from cmon.dataflow.dataflow import Dataflow
from cmon.backend.backend import Backend
from cmon.website.website import Website
from cmon.website.website import URL
from cmon.testsuite import TestSuite
from cmon.dashboard import Dashboard
from cmon.server.server_tests import measure_server_ping
from cmon.server.server_tests import measure_server_ssh_aliveness
from cmon.server.server_tests import measure_server_ssh_mountpoints
from cmon.server.server_tests import measure_server_ssh_sysinfo
from cmon.server.server_tests import measure_server_ssh_docker
from cmon.database.db_tests import measure_db_login
from cmon.database.db_tests import measure_db_size
from cmon.dataflow.dataflow_tests import measure_dataflow_outage
from cmon.website.web_tests import measure_web_urls

# List the normal set of tests we apply to each type of test subject
standard_tests = {
	# A single computer
	Server: [
		measure_server_ping,  # check it pings
		measure_server_ssh_aliveness,  # check basic ssh response
		measure_server_ssh_mountpoints,  # check mountpoints are mounted and not full
		measure_server_ssh_sysinfo,  # read OS, memory avail/used, CPU count and usage, netio, fileio
		measure_server_ssh_docker,
	],
	# A database instance or cluster running on one or more servers
	Database: [
		measure_db_login,  # basic connection
		# measure_db_size,  # size of database
	],
	# A directory or set of directories or heirarchy of directories considered a single flow of data
	Dataflow: [
		measure_dataflow_outage,  # check for last modification / creation
	],
	# A custom service such as an application backend, running on servers, using databases,
	# processing dataflows and providing websites
	Backend: [
	],
	# A website provided by a server
	Website: [
		measure_web_urls,  # website reachableness, header errors, content errors,
	],
}

servers = {
	"webhost": Server(
		label="Website server",
		hostname="192.168.4.10",

	),
	"pghost": Server(
		label="Database server",
		hostname="192.168.4.11",

	),
	"sshhost": Server(
		label="SSH server",
		hostname="192.168.4.12",
		ssh_user="gst4",
		ssh_password="gst4",
	),
}

databases = {
	"postgres": Database(
		dialect="postgresql+psycopg",
		label="Demo Postgres database",
		host=servers["pghost"],
		database="cmon",
		user="pg",
		password="pg",  # should check ~/.pgpass too
	),
}

websites = {
	'website': Website(
		label="Demo website",
		server=servers["webhost"],
		url=[
			URL("http://192.168.4.10", label="Main site address"),
		],
	),
}

dashboards = Dashboards(
	nav_title="Demos",
	nav_url="#",
	nav_tooltip="Return to demos",
	standard_tests=standard_tests,
	dashboards={
		"main": Dashboard(
			label="Main",
			test_suites={
				"servers": TestSuite(
					label="Servers",
					targets=servers,
				),
				"databases": TestSuite(
					label="Databases",
					targets=databases,
				),
				"websites": TestSuite(
					label="Websites",
					targets=websites,
				),
			},
		),
	},
)
