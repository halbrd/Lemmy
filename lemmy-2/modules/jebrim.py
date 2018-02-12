from module import Module
import json
import random
import re

class Jebrim(Module):
	json_location = 'data/jebrim/tweets.json'

	docs = {
		'description': 'Posts random Jebrim quotes'
	}
	def __init__(self, client):
		Module.__init__(self, client)
		json_data = json.load(open(Jebrim.json_location, 'r'))
		self.tweet_list = json_data['links']

	docs_addjebrim = {
		'description': 'Add a new Jebrim screenshot to the list (Imgur direct links only)',
		'usage': 'addjebrim link'
	}
	async def cmd_addjebrim(self, message, args, kwargs):
		if args[0] in self.tweet_list:
			await self.send_error(message)
			return

		if not re.match('https://i\.imgur\.com/[A-Za-z0-9]+\.(png|jpg)/?', args[0]):
			await self.send_error(message)
			return

		self.tweet_list.append(args[0])
		json_data = { 'links' : self.tweet_list }
		json.dump(json_data, open(Jebrim.json_location, 'w'), indent=4)
		await self.send_success(message)

	docs_jebrim = {
		'description': 'Posts a random Jebrim quote'
	}
	async def cmd_jebrim(self, message, args, kwargs):
		await self.client.send_message(message.channel, random.choice(self.tweet_list))
