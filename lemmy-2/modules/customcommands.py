import sys
sys.path.append('..')
from module import Module

import emoji
import re
import io
import json

class CustomCommands(Module):
	docs = {
		'description': 'Posts custom-defined commands'
	}

	BLACKLISTED_EMOJI = set(emoji.UNICODE_EMOJI)

	ALREADY_EXISTS_MESSAGE = lambda name: f'`{name}` is already a command'
	DOES_NOT_EXIST_MESSAGE = lambda name: f'`{name}` is not a command'
	INVALID_NAME_MESSAGE = lambda name: f'`{name}` is an invalid name (must be 20 characters or fewer, no emojis or whitespace)'
	INVALID_VALUE_MESSAGE = lambda value: f'`{value}` is an invalid value'

	def load_commands(self):
		self.commands = self.load_data('commands')

	def save_commands(self):
		self.save_data('commands', self.commands)

	@staticmethod
	def validate_command_name(name):
		# length
		if len(name) > 20:
			return False

		# no emojis or fun allowed
		for character in name:
			if character in CustomCommands.BLACKLISTED_EMOJI:
				return False

		# no whitespace
		if re.search(r'\s', name):
			return False

		return True

	@staticmethod
	def validate_command_value(value):
		if len(value) > 2000:
			# wait, this shouldn't be possible
			return False

		return True

	@staticmethod
	def compress_text(text, max_length=50):
		suffix = '...' if len(text) > max_length else ''
		compressed_text = text.split('\n')[0]
		return compressed_text[:max_length] + suffix

	def create_command(self, name, value):
		if name in self.commands:
			raise ValueError(CustomCommands.ALREADY_EXISTS_MESSAGE(name))

		if not CustomCommands.validate_command_name(name):
			preview = CustomCommands.compress_text(name)
			raise ValueError(CustomCommands.INVALID_NAME_MESSAGE(preview))

		if not CustomCommands.validate_command_value(value):
			preview = CustomCommands.compress_text(value)
			raise ValueError(CustomCommands.INVALID_VALUE_MESSAGE(preview))

		self.commands[name] = value
		self.save_commands()

	def edit_command(self, name, value):
		if not name in self.commands:
			raise ValueError(CustomCommands.DOES_NOT_EXIST_MESSAGE(name))

		if not CustomCommands.validate_command_value(value):
			preview = CustomCommands.compress_text(value)
			raise ValueError(CustomCommands.INVALID_VALUE_MESSAGE(preview))

		self.commands[name] = value
		self.save_commands()

	def delete_command(self, name):
		if not name in self.commands:
			raise ValueError(CustomCommands.DOES_NOT_EXIST_MESSAGE(name))

		del self.commands[name]
		self.save_commands()

	def rename_command(self, old_name, new_name):
		if not old_name in self.commands:
			raise ValueError(CustomCommands.DOES_NOT_EXIST_MESSAGE(old_name))

		if new_name in self.commands:
			raise ValueError(CustomCommands.ALREADY_EXISTS_MESSAGE(new_name))

		if not CustomCommands.validate_command_name(new_name):
			preview = CustomCommands.compress_text(new_name)
			raise ValueError(CustomCommands.INVALID_NAME_MESSAGE(name))

		self.commands[new_name] = self.commands[old_name]
		del self.commands[old_name]
		self.save_commands()

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
		if len(self.commands) == 0:
			await self.client.send_message(message.channel, '```\nNo custom commands.\n```')
			return

		commands = sorted(self.commands.keys(), key=lambda command: (len(command), command))

		table_chunks = self.lemmy.chunk_text(self.lemmy.make_table(commands), chunk_prefix='```\n', chunk_suffix='\n```')

		for chunk in table_chunks:
			await self.client.send_message(message.channel, chunk)

	docs_ccomm_search = {
		'description': 'Lists all custom commands that contain a given string',
		'usage': 'ccomm_search <search term>',
		'examples': [ 'ccomm_search hmmm' ]
	}
	async def cmd_ccomm_search(self, message, args, kwargs):
		if len(args) != 1:
			await self.send_error(message)
			return

		commands = filter(lambda command: args[0] in command, self.commands.keys())
		commands = sorted(commands, key=lambda command: (len(command), command))

		# if the search term is matched exactly, highlight it (needs `md` syntax highlighting)
		commands = [ command if command != args[0] else f'< {args[0]} >' for command in commands ]

		if not commands:
			await self.client.send_message(message.channel, f'```\nNo results.\n```')
			return

		table_chunks = self.lemmy.chunk_text(self.lemmy.make_table(commands), chunk_prefix='```md\n', chunk_suffix='\n```')

		for chunk in table_chunks:
			await self.client.send_message(message.channel, chunk)

	docs_ccomm_create = {
		'description': 'Adds a new custom command',
		'usage': 'ccomm_create <command name> <contents>',
		'examples': [ 'ccomm_create jeffs https://i.imgur.com/biWAU5b.jpg', 'ccomm_create shards "Shards are the secret ingredient in the web scale sauce."' ]
	}
	async def cmd_ccomm_create(self, message, args, kwargs):
		if len(args) != 2:
			await self.send_error(message)
			return

		try:
			self.create_command(args[0], args[1])
		except ValueError as e:
			await self.send_error(message, comment=str(e))
		else:
			await self.send_success(message)

	docs_ccomm_edit = {
		'description': 'Edits the value an existing custom command',
		'usage': 'ccomm_edit <command name> <new contents>',
		'examples': [ 'ccomm_edit terrific http://i.imgur.com/tbdwRyb.gifv' ]
	}
	async def cmd_ccomm_edit(self, message, args, kwargs):
		if len(args) != 2:
			await self.send_error(message)
			return

		try:
			self.edit_command(args[0], args[1])
		except ValueError as e:
			await self.send_error(message, comment=str(e))
		else:
			await self.send_success(message)

	docs_ccomm_delete = {
		'description': 'Deletes an existing custom command',
		'usage': 'ccomm_delete <command name>',
		'examples': [ 'ccomm_delete lenny' ]
	}
	async def cmd_ccomm_delete(self, message, args, kwargs):
		if len(args) != 1:
			await self.send_error(message)
			return

		try:
			self.delete_command(args[0])
		except ValueError as e:
			await self.send_error(message, comment=str(e))
		else:
			await self.send_success(message)

	docs_ccomm_rename = {
		'description': 'Renames an existing custom command',
		'usage': 'ccomm_rename <current name> <new name>',
		'examples': [ 'ccomm_rename kappa greyface' ]
	}
	async def cmd_ccomm_rename(self, message, args, kwargs):
		if len(args) != 2:
			await self.send_error(message)
			return

		try:
			self.rename_command(args[0], args[1])
		except ValueError as e:
			await self.send_error(message, comment=str(e))
		else:
			await self.send_success(message)

	docs_ccomm_dump = {
		'description': 'Dumps all custom commands to a JSON file'
	}
	async def cmd_ccomm_dump(self, message, args, kwargs):
		f = io.StringIO(json.dumps(self.commands, indent='\t'))
		await self.client.send_file(message.channel, f, filename='customcommands.json')
