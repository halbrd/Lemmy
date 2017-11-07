import re

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

	async def send_error(self, message, comment=None):
		await self.client.add_reaction(message, '❌')
		if comment:
			await self.client.send_message(message.channel, comment)

	async def send_success(self, message, comment=None):
		await self.client.add_reaction(message, '✅')
		if comment:
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

	def __init__(self, lemmy):
		self.lemmy = lemmy
		self.client = lemmy.client   # this line is arguably bad taste code, but the name binding removes a *lot* of typing
		self.commands = { function[4:]: getattr(self, function) for function in dir(self) if function.startswith('cmd_') }

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

			if command in self.commands:
				if self.get_docs_attr(command, 'admin_only', default=False) and not message.author.id in self.lemmy.config['admin_users']:
					await self.send_not_allowed(message)
				else:
					try:
						await self.commands[command](message, args[1:], kwargs)
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

	def help_text(self, command=None, symbol=''):
		# if a command is being inspected, verify that it exists
		if command and not hasattr(self, f'cmd_{command}'):
			raise AttributeError(f'Module \'{type(self).__name__}\' has no command \'{command}\'')

		# formulate title
		if not command:   # asking about the module
			syntax = 'md'
			title = f'<module {type(self).__name__}>'
		else:   # asking about a command
			syntax = 'apacheconf'
			title = symbol + (self.get_docs_attr(command, 'usage') or command)
		title = f'```{syntax}\n{title}\n```'

		# formulate description
		description = self.get_docs_attr(command, 'description') if command else self.get_module_docs_attr('description')

		# formulate 'generic list' (examples or list of commands)
		if not command:
			if not self.commands:   # no commands in module
				generic_list = 'This module has no commands'
			else:
				generic_list = 'Commands in this module: ' + ', '.join([f'`{symbol}{command_name}`' for command_name, function in self.commands.items()])
		else:
			examples = self.get_docs_attr(command, 'examples')
			if not examples:
				generic_list = None
			else:
				generic_list = 'Examples: ' + ('\n  ' if len(examples) > 1 else '') + '\n  '.join(f'`{symbol}{example}`' for example in examples)

		# filter Nones out and put the rest into a list
		lines = list(filter(lambda line: line is not None, [title, description, generic_list]))

		# convert to string and return
		return '\n'.join(lines)
