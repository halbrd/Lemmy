from module import Module
import discord

class Core(Module):
	docs = {
		'description': 'Contains basic bot-related functions'
	}

	docs_shutdown = {
		'description': 'Gracefully stops and disconnects Lemmy (requires admin)'
	}
	async def cmd_shutdown(self, message, args, kwargs):
		if message.author.id in self.lemmy.config["admin_users"]:
			self.lemmy.log('Shutting down...')
			await self.send_success(message)
			await self.client.logout()
		else:
			raise Module.CommandNotAllowed

	docs_reload = {
		'description': 'Reloads modules from disk (requires admin)'
	}
	async def cmd_reload(self, message, args, kwargs):
		if message.author.id in self.lemmy.config["admin_users"]:
			self.lemmy.log('Reloading...')

			self.lemmy.load_all_sync()
			await self.lemmy.load_all_async()

			self.lemmy.log('Reloaded.')
			await self.send_success(message)
		else:
			raise Module.CommandNotAllowed

	docs_help = {
		'description': 'Returns documentation for bot functions',
		'usage': 'help <Module or function>',
		'examples': [ 'help', 'help Core', 'help reload' ]
	}
	async def cmd_help(self, message, args, kwargs):
		broadcast = 'broadcast' in kwargs and bool(kwargs['broadcast'])
		symbol = self.lemmy.resolve_symbol(message.channel)

		if len(args) == 0:
			# get our module manifest
			manifest = { module_name: [ command_name for command_name, command in module.commands.items() ] for module_name, module in self.lemmy.modules.items() }

			# construct message initially as a list of lines, for convenience
			lines = []
			lines.append('```diff')

			'''
			Before we start getting any help text, we need to consider what the symbol should be.
			Since, if `broadcast` is false, we will be sending the message to a different channel
			(that is, a direct message) than the one the help command was called from, our `symbol`
			variable might not be accurate. Therefore, if we are sending the help message directly
			to the user, we need to call resolve_symbol again and pass None to get the default symbol.
			'''
			if not broadcast:
				symbol = self.lemmy.resolve_symbol(None)

			for module_name, commands in manifest.items():
				# we want to append the module description if available
				module_description = self.lemmy.modules[module_name].get_module_docs_attr('description')
				module_description = ' - ' + module_description if module_description else ''
				lines.append(f'+ {module_name}{module_description}')

				for command_name in commands:
					# we want to append the command description if available
					command_description = self.lemmy.modules[module_name].get_docs_attr(command_name, 'description')
					command_description = ' - ' + command_description if command_description else ''
					lines.append(f'    {symbol}{command_name}{command_description}')

			lines.append('```')
			lines.append(f'`{symbol}help <Module>` or `{symbol}help <command>` for more info')

			text = '\n'.join(lines)
			if broadcast:
				await self.client.send_message(message.channel, text)
			else:
				if type(message.channel) == discord.channel.PrivateChannel:   # we don't want to add the sent_dm emoji reaction if the user is talking to Lemmy directly
					await self.client.send_message(message.channel, text)
				else:
					await self.send_dm(message, text)
		else:
			topic = args[0]
			help_texts = []

			# user is asking about a module
			if topic in self.lemmy.modules.keys():
				help_texts.append(self.lemmy.modules[topic].help_text(symbol=symbol))

			# user is asking about a command
			else:
				for module_name, module in self.lemmy.modules.items():
					if topic in module.commands.keys():
						help_texts.append(self.lemmy.modules[module_name].help_text(topic, symbol=symbol))

			if not help_texts:
				raise Module.CommandError(f'\'{topic}\' is not a module or command')
			else:
				for help_text in help_texts:
					await self.client.send_message(message.channel, help_text)

	docs_about = {
		'description': 'Contains info about Lemmy'
	}
	async def cmd_about(self, message, args, kwargs):
		title = '```fix\n=========================================\n=  _                                    =\n= | |    ___ _ __ ___  _ __ ___  _   _  =\n= | |   / _ \ \'_ ` _ \| \'_ ` _ \| | | | =\n= | |__|  __/ | | | | | | | | | | |_| | =\n= |_____\___|_| |_| |_|_| |_| |_|\__, | =\n=                                |___/  =\n=========================================\n Your friendly neighbourhood Discord bot\n  Created by https://github.com/halbrd\n```'
		await self.client.send_message(message.channel, title)
