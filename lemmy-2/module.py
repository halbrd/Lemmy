import re
import json
import os

class Module:
	class CommandError(Exception):
		def __init__(self, message=None):
			self.message = message
			super().__init__(message)

	class CommandSuccess(Exception):
		def __init__(self, message=None):
			self.message = message
			super().__init__(message)

	class CommandNotAllowed(Exception):
		def __init__(self, message=None):
			self.message = message
			super().__init__(message)

	class CommandDM(Exception):
		def __init__(self, direct_message, public_message=None):
			self.direct_message = direct_message
			self.public_message = public_message
			super().__init__(direct_message)

	async def send_error(self, message, comment=None, comment_wrapping=True):
		await self.client.add_reaction(message, '❌')
		if comment:
			if comment_wrapping:
				comment = f'```diff\n- {comment}\n```'
			await self.client.send_message(message.channel, comment)

	async def send_success(self, message, comment=None, comment_wrapping=True):
		await self.client.add_reaction(message, '✅')
		if comment:
			if comment_wrapping:
				comment = f'```diff\n+ {comment}\n```'
			await self.client.send_message(message.channel, comment)

	async def send_not_allowed(self, message, comment=None):
		await self.client.add_reaction(message, '🔒')
		if comment:
			await self.client.send_message(message.channel, comment)

	async def send_dm(self, message, direct_message, public_message=None):
		await self.client.add_reaction(message, '📨')
		await self.client.send_message(message.author, direct_message)
		if public_message:
			await self.client.send_message(message.channel, public_message)

	def __init__(self, lemmy, enabled=True):
		self.lemmy = lemmy
		self.client = lemmy.client   # this line is arguably bad taste code, but the name binding removes a *lot* of typing
		self.enabled = enabled

		self._commands = { function[4:]: getattr(self, function) for function in dir(self) if function.startswith('cmd_') }

	async def on_message(self, message):
		if message.author != self.client.user:
			await self.call_functions(message)

	async def call_functions(self, message):
		# get parsed message
		terms = Module.deconstruct_message(message)
		args = terms['args']
		kwargs = terms['kwargs']

		# resolve command symbol
		symbol = self.lemmy.resolve_symbol(message.channel)

		# call command and handle result
		if len(args) > 0 and args[0].startswith(symbol):
			args[0] = args[0][len(symbol):]
			command = args[0].replace('-', '_')

			if command in self._commands:
				# check if the user is permitted to use this command
				if self.get_docs_attr(command, 'admin_only', default=False) and not message.author.id in self.lemmy.config['admin_users']:
					await self.send_not_allowed(message)
				else:
					try:
						await self._commands[command](message, args[1:], kwargs)
					except Module.CommandError as e:
						usage_message = ('Usage: `' + self.get_docs_attr(command, 'usage') + '`') if self.get_docs_attr(command, 'usage') else None
						await self.send_error(message, e.message or usage_message)
					except Module.CommandSuccess as e:
						await self.send_success(message, e.message)
					except Module.CommandNotAllowed as e:
						await self.send_not_allowed(message, e.message)
					except Module.CommandDM as e:
						await self.send_dm(message, e.direct_message, e.public_message)

	@staticmethod
	def deconstruct_message(message):
		# separate message into terms whitespace-delimited terms, preserving quoted sections
		quote = None
		terms = ['']
		for char in message.content:
			# conditions -> actions:
			# quote closed, non-quote character -> add to most recent term
			# quote closed, quote character -> set quote
			# quote closed, whitespace character -> add new term if most recent isn't empty
			# quote open, non-quote character -> add to most recent term
			# quote open, matching quote -> clear quote
			# quote open, non-matching quote -> add to most recent term
			# quote open, whitespace character -> add to most recent term

			# these need to be evaluated before action is taken
			set_quote          = quote is     None  and  char in ['\'', '"', '`']
			clear_quote        = quote is not None  and  char == quote
			add_new_term       = quote is     None  and  char.isspace()            and not terms[-1] == ''
			add_to_most_recent = not any([set_quote, clear_quote, add_new_term])

			if add_to_most_recent:
				terms[-1] += char
			if set_quote:
				quote = char
			if clear_quote:
				quote = None
			if add_new_term:
				terms.append('')

		# remove trailing empty term
		while len(terms) > 0 and terms[-1] == '':
			del terms[-1]

		kwarg_match = re.compile('([a-z]+)=(\S+)|[\'"`](.+)[\'"`]')
		args = [ term for term in terms if not re.fullmatch(kwarg_match, term) ]
		kwargs = { match.group(1): match.group(2) for match in filter(lambda match: match is not None, map(lambda term: re.fullmatch(kwarg_match, term), terms)) }

		return {
			'args': args,
			'kwargs': kwargs
		}

	def get_docs_attr(self, command, attr, default=None):
		try:
			return getattr(self, f'docs_{command}')[attr]
		except (AttributeError, KeyError):
			return default

	def get_module_docs_attr(self, attr, default=None):
		try:
			return getattr(self, 'docs')[attr]
		except (AttributeError, KeyError):
			return default

	def get_help_text(self, command=None, symbol=''):
		# if a command is being inspected, verify that it exists
		if command and not hasattr(self, f'cmd_{command}'):
			raise AttributeError(f'Module \'{type(self).__name__}\' has no command \'{command}\'')

		lines = []

		# asking about a specific command
		if command:
			# title
			lines.append(f'```apacheconf\n' + symbol + (self.get_docs_attr(command, 'usage') or command) + '\n```')
			# description
			lines.append(self.get_docs_attr(command, 'description'))
			# examples
			examples = self.get_docs_attr(command, 'examples')
			if examples:
				lines.append('Examples:\n  ' + '\n  '.join(f'`{symbol}{example}`' for example in examples))

		# asking about the module generally
		# the resultant text should be wrapped in a diff code block by whatever calls for it
		else:
			# title
			name = type(self).__name__
			module_description = self.get_module_docs_attr('description')
			module_description = f' - {module_description}' if module_description else ''
			lines.append(f'{"+" if self.enabled else "-"} {name}{module_description}{"" if self.enabled else " [Disabled]"}')

			# commands - only include if module is enabled
			if self.enabled:
				for command_name in self._commands.keys():
					# we want to append the command description if available
					command_description = self.get_docs_attr(command_name, 'description')
					command_description = ' - ' + command_description if command_description else ''
					lock_or_spaces = '🔒' if self.get_docs_attr(command_name, 'admin_only', default=False) else '  '
					lines.append(f' {lock_or_spaces} {symbol}{command_name}{command_description}')

		# filter Nones out and put the rest into a list
		lines = list(filter(lambda line: line is not None, lines))

		# convert to string and return
		return '\n'.join(lines)

	def load_data(self, document_name):
		target_directory = f'data/{self.__class__.__name__}/'
		target_file = target_directory + f'{document_name}.json'

		# check that directory exists
		if not os.path.isdir(target_directory):
			os.makedirs(target_directory)

		# check that file exists
		if not os.path.isfile(target_file):
			with open(target_file, 'w') as f:
				f.write('{}')

		# get data
		with open(target_file, 'r') as f:
			return json.load(f)

	def save_data(self, document_name, data):
		with open(f'data/{self.__class__.__name__}/{document_name}.json', 'w') as f:
			json.dump(data, f, indent='\t')
