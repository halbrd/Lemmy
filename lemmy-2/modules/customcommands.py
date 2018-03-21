from module import Module

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
		# TODO: check with 0 to columncount-many commands

		# break commands into columns
		column_count = 5
		commands = sorted(self.commands.keys(), key=lambda command: (len(command), command))

		# # left to right, top to bottom
		# columns = [ [] for _ in range(3) ]
		#
		# for i in range(column_count):
		# 	columns[i] = commands[i::column_count]

		# # top to bottom, left to right
		# one_third_point = len(commands) // 3 + 1
		# two_thirds_point = 2 * len(commands) // 3 + 1
		#
		# columns = [
		# 	commands[:one_third_point],
		# 	commands[one_third_point:two_thirds_point],
		# 	commands[two_thirds_point:]
		# ]

		# top to bottom, left to right
		columns = []

		# function to find the index that is the end of the n-1th column and the start of the nth column
		def nth_divider(n):
			return n * len(commands) // column_count

		for i in range(column_count):
			start_index = nth_divider(i)
			end_index = nth_divider(i + 1)
			columns.append(commands[start_index:end_index])


		# add empty entries so longer columns don't get their bottom cells chopped off by zip()
		max_column_length = max([ len(column) for column in columns ])
		for column in columns:
			if len(column) < max_column_length:
				column.append('')

		# pad cell values
		widths = [ max([ len(command) for command in column ]) for column in columns ]

		for i, column in enumerate(columns[:-1]):   # don't need to pad the last column; should save us some characters
			for j in range(len(column)):
				columns[i][j] = columns[i][j] + ' ' * (widths[i] - len(columns[i][j]))

		# convert to rows
		rows = list(zip(*columns))
		rows = [ '  '.join(row) for row in rows ]

		# chunk rows to avoid 2000 character limit
		character_limit = 2000
		extra_characters = len('```\n\n```')

		chunks = [ [] ]
		for row in rows:
			if sum([ len(row) for row in chunks[-1] ]) + len('\n' * len(chunks[-1])) + extra_characters + len(row) <= character_limit:   # there's still room
				chunks[-1].append(row)
			else:
				chunks.append([row])

		# send chunks
		for rows in chunks:
			r = '```\n' + '\n'.join(rows) + '\n```'
			print(len(r))
			print(r)
			await self.client.send_message(message.channel, r)

	docs_ccomm_search = {
		'description': 'Searches for a custom command',
		'usage': 'ccomm_search search_term',
		'examples' [ 'ccomm_search ttt' ]
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
