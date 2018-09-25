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
import logging
import signal
import io

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
			channel = message.channel

			if type(channel) == discord.channel.DMChannel:
				recipient = channel.recipient.name if message.author == channel.me else channel.me.name
			elif type(channel) == discord.channel.GroupChannel:   # bot users can't be in these (yet)
				recipient = channel.name or ', '.join( list( { user.name for user in message.channel.recipients }.union({ self.client.user.name }) - { message.author.name } ) )
			elif type(channel) == discord.channel.TextChannel:
				recipient = f'{channel.guild}#{channel.name}'

			extras_phrase = '📎' * len(message.attachments) + '📊' * len(message.embeds)
			extras_phrase = f' +{extras_phrase}' if extras_phrase else ''

			self.log(f'{message.author.name} => {recipient}{extras_phrase}: {message.content}')

			# pass the event to the modules
			for _, module in self.modules.items():
				await module.on_message(message)

		@self.client.event
		async def on_ready():
			# perform asynchronous setup
			await self.load_all_async()

			# pass the event to the modules
			for _, module in self.modules.items():
				await module.on_ready()

			self.log('Logged in.')

		# log in
		self.log('Logging in...')

		# run the bot
		loop = asyncio.get_event_loop()

		# enable the bot to respond to SIGINT/SIGTERM (Unix only)
		try:
			loop.add_signal_handler(signal.SIGINT, lambda: asyncio.ensure_future(self.handle_sigint()))
			loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.ensure_future(self.handle_sigterm()))
		except NotImplementedError:
			pass   # Lemmy is running in Windows - nothing we can do

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

		self.logger.info(output)

	def load_all_sync(self):
		self.load_config()
		self.load_modules()
		self.setup_logging()

	async def load_all_async(self):
		await self.load_playing_message()

	def load_config(self):
		if not os.path.isfile('config.json'):
			raise Lemmy.NoConfigException

		self.config = json.load(open('config.json', 'r'))

	def load_modules(self):
		self.modules = {}

		for module_class_name in self.config['default_manifest']:
			module = importlib.import_module(module_class_name.lower())
			importlib.reload(module)   # changes to the module will be loaded (for if this was called again while the bot is running)
			class_ = getattr(module, module_class_name)
			self.modules[module_class_name] = class_(self)

	async def load_playing_message(self):
		await self.client.change_presence(activity=discord.Game(name=self.get_config_key_or_default('playing_message')))

	def setup_logging(self):
		logging.basicConfig(format='%(message)s', level=logging.WARNING)

		self.logger = logging.getLogger('lemmy')
		self.logger.setLevel(logging.INFO)

		if self.config['log_file']:
			self.logger.addHandler(logging.FileHandler(self.config['log_file']))

	async def shutdown(self):
		self.log('Shutting down...')
		await self.client.logout()

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
			return self.get_config_key_or_default("server_config", channel.guild.id, "symbol", default=default_symbol)
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

	async def handle_sigint(self):
		self.log('Received SIGINT.')
		await self.shutdown()

	async def handle_sigterm(self):
		self.log('Received SIGTERM.')
		await self.shutdown()

	def to_discord_file(self, contents, file_name):
		if type(contents) == bytes:
			contents = io.BytesIO(contents)
		elif type(contents) == str:
			contents = io.StringIO(contents)

		return discord.File(fp=contents, filename=file_name)

	async def send_text_file(self, body, destination, file_name='text.txt', comment=None):
		file = self.to_discord_file(body, file_name)
		await destination.send(comment, file=file)



if __name__ == '__main__':
	if not os.path.isfile('config.json'):
		raise Lemmy.NoConfigException

	lemmy = Lemmy(json.load(open('config.json', 'r'))['token'])
