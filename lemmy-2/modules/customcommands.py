from module import Module

from itertools import zip_longest

class CustomCommands(Module):
	docs = {
		'description': 'Posts custom-defined commands'
	}

	def load_commands(self):
		self.commands = self.load_data('commands')

	def save_commands(self):
		self.save_data('commands', self.commands)

	def __init__(self, client):
		Module.__init__(self, client)

		self.load_commands()

	async def on_message(self, message):
		# perform normal command execution
		if message.author != self.client.user:
			await self.call_functions(message)

		# respond to custom commands
		if message.author != self.client.user:
			# reusing code from Module.call_functions, unfortunately
			terms = Module.deconstruct_message(message)
			args = terms['args']
			kwargs = terms['kwargs']

			# resolve command symbol
			symbol = self.lemmy.resolve_symbol(message.channel)

			# call command and handle result
			if len(args) > 0 and args[0].startswith(symbol):
				args[0] = args[0][len(symbol):]
				command = args[0]

				if command in self.commands:
					await self.client.send_message(message.channel, self.commands[command])

	docs_ccomm_list = {
		'description': 'Lists all custom commands'
	}
	async def cmd_ccomm_list(self, message, args, kwargs):
		column_count = 6
		commands = sorted(self.commands.keys(), key=lambda command: (len(command), command))

		# determine how many elements are in each column
		column_base_length = len(commands) // column_count
		column_extra_count = len(commands) % column_count
		column_lengths = [ column_base_length for _ in range(column_count) ]
		# add the extras to the end of the relevant columns
		for i in range(column_extra_count):
			column_lengths[i] += 1

		print(column_lengths)

		# assemble columns
		columns = []
		for column_index in range(len(column_lengths)):
			column_start_index = sum(column_lengths[:column_index])
			column_end_index = sum(column_lengths[:column_index + 1])
			columns.append(commands[column_start_index:column_end_index])

		# pad elements
		for i, column in enumerate(columns):
			column_width = max([ len(element) for element in column ])
			for j, element in enumerate(column):
				columns[i][j] = element + ' ' * (column_width - len(element))

		# assemble rows
		rows = [ list(row) for row in zip_longest(*columns) ]

		# remove any Nones added by zip_longest from the last row
		while rows[-1][-1] is None:
			rows[-1].pop()

		from pprint import pprint
		pprint(rows)

		# convert rows to text
		text = '\n'.join([ '  '.join(row) for row in rows ])
		text = f'```\n{text}\n```'

		await self.client.send_message(message.channel, text)

	docs_ccomm_search = {
		'description': 'Searches for a custom command',
		'usage': 'ccomm_search search_term',
		'examples': [ 'ccomm_search hmmm' ]
	}
	async def cmd_ccomm_search(self, message, args, kwargs):
		return

	@staticmethod
	def validate_command_name(name):
		# allow only ASCII characters
		if not all(ord(char) < 128 for char in name):
			return False

		return True

	@staticmethod
	def validate_command_value(value):
		return True

	docs_ccomm_add = {
		'description': 'Adds a new custom command',
		'usage': 'ccomm_add command_name contents',
		'examples': [ 'ccomm_add lenny ( ͡° ͜ʖ ͡°)' ]
	}
	async def cmd_ccomm_add(self, message, args, kwargs):
		if len(args) != 2:
			self.send_error(message)
			return

		if args[0] in self.commands:
			self.send_error(message, comment=f'`{args[0]}` is already a command')
			return

		if not CustomCommands.validate_command_name(args[0]):
			self.send_error(message, comment=f'`{args[0]}` is an invalid name')
			return

		if not CustomCommands.validate_command_value(args[1]):
			self.send_error(message, comment=f'`{args[1]}` is an invalid value')
			return

		self.commands[args[0]] = args[1]
		self.save_commands()
		self.send_success(message)

	docs_ccomm_edit = {
		'description': 'Edits an existing custom command',
		'usage': 'ccomm_edit command_name new_contents',
		'examples': [ 'ccomm_edit lenny ( ͡ಠ ʖ̯ ͡ಠ)' ]
	}
	async def cmd_ccomm_edit(self, message, args, kwargs):
		if len(args) != 2:
			self.send_error(message)
			return

		if not args[0] in self.commands:
			self.send_error(message, comment=f'`{args[0]}` is not a command')
			return

		self.commands[args[0]] = args[1]
		self.save_commands()
		self.send_success(message)

	docs_ccomm_delete = {
		'description': 'Deletes and existing custom command',
		'usage': 'ccomm_delete command_name',
		'examples': [ 'ccomm_delete lenny' ]
	}
	async def cmd_ccomm_delete(self, message, args, kwargs):
		if len(args) != 1:
			self.send_error(message)
			return

		if not args[0] in self.commands:
			self.send_error(message, comment=f'`{args[0]}` is not a command')
			return

		del self.commands[args[0]]
		self.save_commands()
		self.send_success(message)
