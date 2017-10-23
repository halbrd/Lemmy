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
		try:
			symbol = self.lemmy.config_try_key("server_config", message.channel.server.id, "symbol")
		except ( AttributeError, KeyError ):
			symbol = self.lemmy.config["default_symbol"]

		# call command and handle result
		if len(args) > 0 and args[0].startswith(symbol):
			args[0] = args[0][len(symbol):]

			if args[0] in self.commands:
				try:
					await self.commands[args[0]](message, args[1:], kwargs)
				except Module.CommandError as e:
					usage_message = 'Usage:\n' + '\n'.join(['`' + form + '`' for form in getattr(self, f'cmd_{args[0]}_usage')])
					await self.send_error(message, e.message or usage_message)
				except Module.CommandSuccess as e:
					await self.send_success(message, e.message)
				except Module.CommandNotAllowed as e:
					await self.send_not_allowed(message, e.message)

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