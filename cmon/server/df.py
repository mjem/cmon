#!/usr/bin/env python3

"""Implementation of decode_df() function.
"""

from collections import namedtuple
from typing import Iterable

# Information about a mounted partition
MountInfo = namedtuple("MountInfo", "filesystem total used free percent mountpoint")

def decode_df(lines:Iterable[str]):
	"""Decode output of a `df` command.

	Works with standard Linux df, local and nfs mounts."""
	# List of (column heading, MuontInfo attribute name, datatype, multiply by bock size)
	search_columns = [["Filesystem", "filesystem", str, False],
					  ["1K-blocks", "total", int, True],
					  ["Used", "used", int, True],
					  ["Available", "free", int, True],
					  ["Use%", "percent", str, False],
					  ["Mounted", "mountpoint", str, False]]
	blocksize = 1024

	process_columns = None
	result = {}
	for line in lines:
		# print("LINE", line, "len", len(line))
		if len(line) == 0:
			# print("skip")
			continue

		cells = line.split()
		if process_columns is None:
			# print("Decode column headings from", line)
			process_columns = []
			# first line
			for heading in cells:
				# print("Identifying heading", heading)
				locate_column = None
				for search_column in search_columns:
					if search_column[0].lower() in heading.lower():
						# print("It is", search_column)
						locate_column = search_column

				process_columns.append(locate_column)

			# print("Decoded", process_columns)
			continue

		mount_parts = {}
		for cell, column in zip(cells, process_columns):
			if column is not None:
				value = column[2](cell)
				if column[3]:
					value *= blocksize

				mount_parts[column[1]] = value

		# print("mount parts", mount_parts)
		mount_info = MountInfo(**mount_parts)
		result[mount_info.mountpoint] = mount_info

	return result

if __name__ == "__main__":
	import pprint
	pprint.pprint(
		decode_df("""Filesystem      1K-blocks       Used  Available Use% Mounted on
udev             16272268          0   16272268   0% /dev
tmpfs             3259640       2728    3256912   1% /run
/dev/nvme0n1p2 1237425072  907315824  271957300  77% /
tmpfs            16298180      51324   16246856   1% /dev/shm
tmpfs                5120          8       5112   1% /run/lock
tmpfs            16298180      16108   16282072   1% /tmp
tmpfs            16298180          0   16298180   0% /var/tmp
/dev/sdc1      5860520960 3112629820 2739245540  54% /mnt/store_a
/dev/sda1      7814025216 3825308656 3987847312  49% /mnt/store_b
tmpfs             3259636       2568    3257068   1% /run/user/1000
/dev/nvme0n1p5  104857600    6787000   96415048   7% /mnt/p5
""".split("\n")))
