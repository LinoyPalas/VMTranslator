"""
Encoder.py
---------------
	- Receive single command from the file.
	- Code the single command.
	- Return the coded command as a list of strings.
"""


class Encoder:
	# Indexes in the command structure: -command- -segment- -index-
	CMD_IND = 0
	SEGMENT_IND = 1
	INDEX_IND = 2

	def __init__(self, file_name):
		"""
		:param file_name: The name of the file we are working on.
		Used when using the 'static' segment.
		"""
		self._file_name = file_name
		self._coded_command = []

		# Dictionary which describes the code_command command of each command.
		self._commands_dict = {
					'push': 'C_PUSH',
					'pop': 'C_POP',
					'add': 'C_ARITHMETIC',
					'sub': 'C_ARITHMETIC',
					'neg': 'C_ARITHMETIC',
					'eq': 'C_ARITHMETIC',
					'gt': 'C_ARITHMETIC',
					'lt': 'C_ARITHMETIC',
					'and': 'C_ARITHMETIC',
					'or': 'C_ARITHMETIC',
					'not': 'C_ARITHMETIC'
					}

		# Dictionary describes the address in memory of each symbol.
		self._addresses_dict = {
			'stack_pointer': 'SP',  # R0
			'local': 'LCL',  # R1
			'argument': 'ARG',  # R2
			'this': 'THIS',  # R3
			'that': 'THAT',  # R4
			'pointer': 3,  # R3 - R4
			'temp': 5,  # R5 - R12
			'static': 16  # 16 - 255
		}

	def get_command_type(self, row):
		return self._commands_dict[row[Encoder.CMD_IND]]

	"""
	-----------
	Pop and Push.
	"""
	def _write_address_commands(self, segment, index):
		segment_address_in_memory = self._addresses_dict[segment]

		if segment == 'constant':  # No specific memory address.
			self._coded_command.append('@' + str(index))

		elif segment in ['local', 'argument', 'this', 'that']:  # R1 - R4
			self._coded_command += [
									'@' + segment_address_in_memory,
									'D=M',
									'@' + str(index),
									'A=D+A'
									]

		elif segment in ['pointer', 'temp']:  # R3 - R4, R5 - R12
			self._coded_command.append('@R' + str(segment_address_in_memory + index))

		elif segment == 'static':  	# 16 - 255
			self._coded_command.append('@' + self._file_name + '.' + str(index))

		else:
			raise Exception('EncoderError - No such segment!')

	def _write_push_pop(self, command, segment, index):
		# First set the addresses based on the segment and the index.
		self._write_address_commands(segment, index)

		if command == 'C_PUSH':
			# Second - define the register.
			reg_operation = 'D=A' if segment == 'constant' else 'D=M'
			self._coded_command.append(reg_operation)
			# Third - add one to the stack pointer.
			self._coded_command += [
									'@SP',
									'A=M',
									'M=D',
									'@SP',
									'M=M+1'
									]

		elif command == 'C_POP':
			self._coded_command += [
									# Part 1 - Load D register to the right address and store the value
									# in the spare (R13-R15) memory location.
									'D=A',
									'@R13',
									'M=D',
									# Part 2 - Reduce 1 from stack pointer and store value in D.
									'@SP',
									'M=M-1',
									'A=M',
									'D=M',
									# Part 3
									'@R13',
									'A=M',
									'M=D'
									]

		else:
			raise Exception('Undefined Command.')

	"""
	-----------
	Arithmetic and Logic.
	"""
	def _write_arithmetic(self, command):
		return

	"""
	-----------
	Main Method.
	Receives the command to code_command and returns the coded commands in a list.
	"""
	def code_command(self, command):
		command_type = self.get_command_type(command)

		if command_type == 'C_ARITHMETIC':
			self._write_arithmetic(command)

		elif command_type in ['C_PUSH', 'C_POP']:
			self._write_push_pop(
								command=command_type,
								segment=command[Encoder.SEGMENT_IND],
								index=command[Encoder.INDEX_IND])

		else:
			raise Exception('EncoderError - No such command!')

		to_return = self._coded_command
		self._coded_command.clear()
		return to_return
