"""
Parser.py
---------------
	- Reads all the rows of the files.
	- Trim the rows.
	- Ignore commands.
	- return the rows as a list.
"""


class Parser:
	def __init__(self):
		self._rows = None
		self._rows_broken_to_commands = []

	def _read_rows(self, vm_file):
		with open(vm_file) as f:
			self._rows = f.readlines()
		self._rows = [row.strip() for row in self._rows]

	def _remove_empty_lines(self):
		self._rows = [row for row in self._rows if row != '']

	def _remove_comments(self):
		self._rows = [row.split("//")[0].strip() for row in self._rows]

	def _break_rows_to_commands(self):
		for row in self._rows:
			broken_row = row.split(' ')
			broken_row = [word.strip for word in broken_row]
			self._rows_broken_to_commands.append(broken_row)

	def parse(self, vm_file):
		self._read_rows(vm_file)
		self._remove_comments()
		self._remove_empty_lines()
		self._break_rows_to_commands()
		return self._rows_broken_to_commands
