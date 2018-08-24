import sys
sys.path.append('..')
from module import Module

import discord

class Core(Module):
	docs = {
		'description': 'Contains basic bot-related functions'
	}

	docs_shutdown = {
		'description': 'Gracefully stops and disconnects Lemmy',
		'admin_only': True
	}
	async def cmd_shutdown(self, message, args, kwargs):
		await self.send_success(message)
		await self.lemmy.shutdown()

	docs_reload = {
		'description': 'Reloads modules from disk',
		'admin_only': True
	}
	async def cmd_reload(self, message, args, kwargs):
		self.lemmy.log('Reloading...')

		self.lemmy.load_all_sync()
		await self.lemmy.load_all_async()

		self.lemmy.log('Reloaded.')
		await self.send_success(message)

	docs_help = {
		'description': 'Returns documentation for bot functions',
		'usage': 'help <Module or function>',
		'examples': [ 'help', 'help Core', 'help reload' ]
	}
	async def cmd_help(self, message, args, kwargs):
		broadcast = 'broadcast' in kwargs and bool(kwargs['broadcast'])
		symbol = self.lemmy.resolve_symbol(message.channel)

		# general help text
		if len(args) == 0:
			# get our module manifest
			manifest = { module_name: [ command_name for command_name, command in module._commands.items() ] for module_name, module in self.lemmy.modules.items() }

			# construct message initially as a list of lines, for convenience
			lines = []

			'''
			Before we start getting any help text, we need to consider what the symbol should be.
			Since, if `broadcast` is false, we will be sending the message to a different channel
			(that is, a direct message) than the one the help command was called from, our `symbol`
			variable might not be accurate. Therefore, if we are sending the help message directly
			to the user, we need to call resolve_symbol again and pass None to get the default symbol.
			'''
			if not broadcast:
				symbol = self.lemmy.resolve_symbol(None)

			for module_name in manifest.keys():
				lines.append(self.lemmy.modules[module_name].get_help_text(symbol=symbol))

			text = '\n'.join(lines)

			chunks = self.lemmy.chunk_text(text, chunk_prefix='```diff\n', chunk_suffix='```')

			footer_message = f'`{symbol}help <Module>` or `{symbol}help <command>` for more info'
			if len(chunks[-1] + '\n' + footer_message) <= 2000:
				chunks[-1] += '\n' + footer_message
			else:
				chunks.append(footer_message)

			for chunk in chunks:
				await message.channel.send(chunk)

		# help text pertaining to a specific topic
		else:
			topic = args[0].replace('-', '_')
			help_texts = []

			# check if user is asking about a module
			if topic in self.lemmy.modules.keys():
				help_texts.append('```diff\n' + self.lemmy.modules[topic].get_help_text(symbol=symbol) + '\n```' + f'\n`{symbol}help <command>` for more info')

			# check if user is asking about a command
			for module_name, module in self.lemmy.modules.items():
				if topic in module._commands.keys():
					help_texts.append(self.lemmy.modules[module_name].get_help_text(topic, symbol=symbol))

			if not help_texts:
				raise Module.CommandError(f'\'{topic}\' is not a module or command')
			else:
				for help_text in help_texts:
					await message.channel.send(help_text)

	docs_about = {
		'description': 'Contains info about Lemmy'
	}
	async def cmd_about(self, message, args, kwargs):
		title = '```fix\n=========================================\n=  _                                    =\n= | |    ___ _ __ ___  _ __ ___  _   _  =\n= | |   / _ \ \'_ ` _ \| \'_ ` _ \| | | | =\n= | |__|  __/ | | | | | | | | | | |_| | =\n= |_____\___|_| |_| |_|_| |_| |_|\__, | =\n=                                |___/  =\n=========================================\n Your friendly neighbourhood Discord bot\n  Created by https://github.com/halbrd\n```'
		repo_link = '  Lemmy is free and open source software, hosted at\nhttps://github.com/halbrd/Lemmy. Bug reports and\n                       pull requests are welcome.'
		await message.channel.send(title + '\n' + repo_link)
