import discord
import datetime
import asyncio
import os
import os.path
import json
import importlib
import sys
import re
from itertools import zip_longest

sys.path.append('modules')

class Lemmy:
	class NoConfigException(Exception):
		def __init__(self, message='config.json does not exist (create it from config.example.json)'):
			super().__init__(message)

	def __init__(self, token):
		# perform setup that should not be performed again (i.e. in a reload)
		self.client = discord.Client()

		# perform synchronous setup
		self.load_all_sync()

		# register events
		@self.client.event
		async def on_message(message):
			context = message.channel.server.name if not type(message.channel) == discord.channel.PrivateChannel else None
			recipient = '#' + message.channel.name if not type(message.channel) == discord.channel.PrivateChannel else ', '.join( list( { user.name for user in message.channel.recipients }.union({ self.client.user.name }) - { message.author.name } ) )

			context_phrase = f'({context}) ' if context else ''
			attachments_phrase = ' +' + '📎' * len(message.attachments) if len(message.attachments) > 0 else ''

			self.log(f'{context_phrase}{message.author.name} => {recipient}{attachments_phrase}: {message.content}')

			# pass the event to the modules
			for _, module in self.modules.items():
				await module.on_message(message)

		@self.client.event
		async def on_ready():
			# perform asynchronous setup
			await self.load_all_async()

			self.log('Logged in.')

		# log in
		self.log('Logging in...')

		# run the bot
		loop = asyncio.get_event_loop()
		try:
			loop.run_until_complete(self.client.start(token))
		except KeyboardInterrupt:
			loop.run_until_complete(self.client.logout())
		finally:
			loop.close()

		# at this point the bot has shut down
		self.log('Shut down.')

	def log(self, message):
		output = '[{}] {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message)

		print(output)

		if self.config['log_file']:
			with open(self.config['log_file'], 'a', encoding='utf8') as f:
				f.write(output + '\n')

	def load_all_sync(self):
		self.load_config()
		self.load_modules()

	async def load_all_async(self):
		await self.load_playing_message()

	def load_config(self):
		if not os.path.isfile('config.json'):
			raise NoConfigException

		self.config = json.load(open('config.json', 'r'))

	def load_modules(self):
		self.modules = {}
		manifest = json.load(open('modules/manifest.json', 'r'))

		for module_class_name, module_info in manifest.items():
			module = importlib.import_module(module_class_name.lower())
			importlib.reload(module)   # changes to the module will be loaded (for if this was called again while the bot is running)
			class_ = getattr(module, module_class_name)
			self.modules[module_class_name] = class_(self, enabled=module_info['enabled'])

	async def load_playing_message(self):
		await self.client.change_presence(game=discord.Game(name=self.get_config_key_or_default('playing_message')))

	def get_config_key_or_default(self, *path, default=None):
		node = self.config
		for step in path:
			if type(node) == dict and step in node:
				node = node[step]
			else:
				return default

		return node

	def resolve_symbol(self, channel):
		default_symbol = self.config["default_symbol"]
		try:
			return self.get_config_key_or_default("server_config", channel.server.id, "symbol", default=default_symbol)
		except AttributeError:
			return default_symbol

	def chunk_text(self, text, chunk_length=2000, chunk_prefix='', chunk_suffix=''):
		rows = text.splitlines()

		# for the time being, we're only going to break on linebreaks
		if max([ len(row) for row in rows ]) + len(chunk_prefix) + len(chunk_suffix) > chunk_length:
			raise ValueError('one or more rows exceed 2000 characters (with prefix and suffix)')

		chunks = []
		while rows:
			if chunks and len(chunk_prefix + chunks[-1] + '\n' + rows[0] + chunk_suffix) <= chunk_length:
				chunks[-1] += '\n' + rows[0]
			else:
				chunks.append(rows[0])
			del rows[0]

		# append prefixes and suffixes
		for i in range(len(chunks)):
			chunks[i] = chunk_prefix + chunks[i] + chunk_suffix

		return chunks

	@staticmethod
	def make_table(elements, column_count=6):
		# if there are fewer elements to display than column_count, we need to reduce column_count to match
		if len(elements) < column_count:
			column_count = len(elements)

		# determine how many elements are in each column
		column_base_length = len(elements) // column_count
		column_extra_count = len(elements) % column_count
		column_lengths = [ column_base_length for _ in range(column_count) ]
		# add the extras to the end of the relevant columns
		for i in range(column_extra_count):
			column_lengths[i] += 1

		# assemble columns
		columns = []
		for column_index in range(len(column_lengths)):
			column_start_index = sum(column_lengths[:column_index])
			column_end_index = sum(column_lengths[:column_index + 1])
			columns.append(elements[column_start_index:column_end_index])

		# pad elements
		for i, column in enumerate(columns[:-1]):
			column_width = max([ len(element) for element in column ])
			for j, element in enumerate(column):
				columns[i][j] = element + ' ' * (column_width - len(element))

		# assemble rows
		rows = [ list(row) for row in zip_longest(*columns) ]

		# remove any Nones added by zip_longest from the last row
		while rows[-1][-1] is None:
			rows[-1].pop()

		# convert rows to text
		return '\n'.join([ '  '.join(row) for row in rows ])



if __name__ == '__main__':
	if not os.path.isfile('config.json'):
		raise Lemmy.NoConfigException

	lemmy = Lemmy(json.load(open('config.json', 'r'))['token'])
