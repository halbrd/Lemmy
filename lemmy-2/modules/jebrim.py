from module import Module
import json
import random

class jebrim(Module):
	jsonKey = 'jebrimLinks'
	jsonLocation = 'modules/jebrimTweets.json'

	docs = {
		'description': 'Posts jebrim tweets'
	}

	def __init__(self, client):
		Module.__init__(self, client)
		jsonData = json.load(open(jebrim.jsonLocation,'r'))
		self.tweetList = jsonData[jebrim.jsonKey]


	docs_addjebrim = {
		'description': 'add link to jebrim tweet to the list'
	}

	async def cmd_addjebrim(self, message, args, kwargs):
		if args[0] in self.tweetList:
			await self.send_error(message)
		else:
			if not args[0].startswith("http"):
				await self.send_error(message)
				await self.client.send_message(message.channel, "Please send valid link")
			else:
				self.tweetList.append(args[0])
				await self.send_success(message)
				jsonData = {jebrim.jsonKey : self.tweetList}
				json.dump(jsonData, open(jebrim.jsonLocation , 'w'))

	docs_jebrim = {
		'description': 'Posts jebrim tweet'
	}

	async def cmd_jebrim(self, message, args, kwargs):
		await self.client.send_message(message.channel, random.choice(self.tweetList))
