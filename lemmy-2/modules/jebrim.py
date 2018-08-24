import sys
sys.path.append('..')
from module import Module

import json
import random
import re
import requests

class Jebrim(Module):
	docs = {
		'description': 'Posts random Jebrim quotes'
	}

	def get_tweets(self):
		return self.load_data('tweets', static=True, default='[]')

	docs_jebrim_add = {
		'description': 'Adds a new Jebrim screenshot to the list',
		'usage': 'jebrim_add <link>'
	}
	async def cmd_jebrim_add(self, message, args, kwargs):
		if len(args) != 1:
			await self.send_error(message)
			return

		if not re.match('https://i\.imgur\.com/[A-Za-z0-9]+\.(png|jpg)/?', args[0]):
			await self.send_error(message, comment='link must be an Imgur direct link')
			return

		tweets = self.get_tweets()

		if args[0] in tweets:
			await self.send_error(message, comment='link already exists in database')
			return

		tweets.append(args[0])
		self.save_data('tweets', tweets, static=True)
		await self.send_success(message)

	docs_jebrim = {
		'description': 'Posts a random Jebrim quote'
	}
	async def cmd_jebrim(self, message, args, kwargs):
		tweets = self.get_tweets()

		if len(tweets) == 0:
			await self.send_error(message, 'Jebrim database is empty')
		else:
			await message.channel.send(random.choice(tweets))

	docs_is_jebrim_suspended = {
		'description': 'Checks if Jebrim is suspended on Twitter'
	}
	async def cmd_is_jebrim_suspended(self, message, args, kwargs):
		if 'This account has been suspended' in requests.get('https://twitter.com/jebrim').text:
			await message.channel.send('Yes, Jebrim is suspended from Twitter.')
		else:
			await message.channel.send('No, Jebrim is not suspended from Twitter! :tada:')
