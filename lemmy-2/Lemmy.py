import discord
import datetime
import asyncio
import os.path
import json

class NoConfigException(Exception):
	def __init__(self, message=None):
		if message is None:
			message = 'config.json does not exist (create it from config.example.json)'

		super(NoConfigException, self).__init__(message)

class Lemmy:
	def log(self, message):
		output = '[{}] {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message)

		print(output)

		if self.config['log_file']:
			with open(self.config['log_file'], 'a') as f:
				f.write(output + '\n')

	def __init__(self, token):
		self.client = discord.Client()

		# import config
		if not os.path.isfile('config.json'):
			raise NoConfigException

		self.config = json.load(open('config.json', 'r'))

		# register events
		@self.client.event
		async def on_message(message):
			self.log(f'({message.channel.server.name}) {message.author.name} => #{message.channel.name}: {message.content}')

			if message.content == '$shutdown' and message.author.id == '77041679726551040':
				await self.client.logout()

		@self.client.event
		async def on_ready():
			self.log('Logged in.')

		# log in
		self.log('Logging in...')
		self.client.run(token)

if __name__ == '__main__':
	if not os.path.isfile('config.json'):
		raise NoConfigException
	lemmy = Lemmy(json.load(open('config.json', 'r'))['token'])
