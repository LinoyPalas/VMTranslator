"""
VMTranslator.py
---------------
"""
import sys
from Parser import Parser
from Encoder import Encoder


class VMTranslator:
	def __init__(self, vm_file):
		self.vm_file = vm_file
		self._parser = Parser()
		self._commands_to_code = self._parser.parse(vm_file)
		self._encoder = Encoder()

	@staticmethod
	def write_commands_to_file(file_name, commands):
		file_name = file_name.split('.vm')[0] + ".asm"
		f = open(file_name, "w+")
		for row in commands:
			f.write(row + '\n')
		f.close()

	def run(self):
		encoded_commands = self._encoder.code_command(self._commands_to_code)
		VMTranslator.write_commands_to_file(file_name=self.vm_file, commands=encoded_commands)


if __name__ == '__main__':
	vm_file = sys.argv[1]
	translator = VMTranslator(vm_file=vm_file)
	translator.run()
