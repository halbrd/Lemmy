import sys
sys.path.append('..')
from module import Module

import json
import random
import re

class Jebrim(Module):
	docs = {
		'description': 'Posts random Jebrim quotes'
	}
	def __init__(self, client):
		Module.__init__(self, client)

		self.tweets = self.load_data('tweets')['links']

	docs_jebrim_add = {
		'description': 'Adds a new Jebrim screenshot to the list',
		'usage': 'jebrim_add <link>'
	}
	async def cmd_jebrim_add(self, message, args, kwargs):
		if args[0] in self.tweets:
			await self.send_error(message, comment='link already exists in database')
			return

		if not re.match('https://i\.imgur\.com/[A-Za-z0-9]+\.(png|jpg)/?', args[0]):
			await self.send_error(message, comment='link must be an Imgur direct link')
			return

		self.tweets.append(args[0])
		data = { 'links' : self.tweets }
		self.save_data('tweets', data)
		await self.send_success(message)

	docs_jebrim = {
		'description': 'Posts a random Jebrim quote'
	}
	async def cmd_jebrim(self, message, args, kwargs):
		await self.client.send_message(message.channel, random.choice(self.tweets))
