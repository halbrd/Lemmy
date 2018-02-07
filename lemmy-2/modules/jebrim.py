from module import Module
import json
import random
import re

class Jebrim(Module):
	json_key = 'jebrim_links'
	json_location = 'modules/jebrim_tweets.json'

	docs = {
		'description': 'Posts random jebrim tweets'
	}

	def __init__(self, client):
		Module.__init__(self, client)
		jsonData = json.load(open(Jebrim.json_location, 'r'))
		self.tweet_list = jsonData[Jebrim.json_key]


	docs_addjebrim = {
		'description': 'Add link to Jebrim tweet to the list'
	}

	async def cmd_addjebrim(self, message, args, kwargs):
		if args[0] in self.tweet_list:
			await self.send_error(message)
		else:
			if not re.match('https?://', args[0]):
				await self.send_error(message, comment='Please send valid link')
				return

			self.tweet_list.append(args[0])
			jsonData = {Jebrim.json_key : self.tweet_list}
			json.dump(jsonData, open(Jebrim.json_location, 'w'), indent=4)
			await self.send_success(message)

	docs_jebrim = {
		'description': 'Posts random Jebrim tweet'
	}

	async def cmd_jebrim(self, message, args, kwargs):
		await self.client.send_message(message.channel, random.choice(self.tweet_list))
