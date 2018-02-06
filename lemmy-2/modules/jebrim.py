from module import Module
import json
import random

class jebrim(Module):

	docs = {
		'description': 'Posts jebrim tweets'
	}

	tweetList = [];
	jsonKey = 'jebrimLinks'
	jsonLocation = 'jebrimTweets.json'

	def __init__(self, client):
		Module.__init__(self, client)
		jsonData = json.load(open(jsonLocation,r))
		tweetList = jsonData[jsonKey]


	docs_addjebrim = {
		'description': 'add link to jebrim tweet to the list'
	}

	async def cmd_addjebrim(self, message, args, kwargs):
		tweetList.append(args[1])
		jsonData = {jsonKey : jsonLocation}
		json.dump(jsonData, open(jsonLocation , 'w'))

	docs_jebrim = {
		'description': 'Posts jebrim tweet'
	}

	async def cmd_jebrim(self, message, args, kwargs):
		await self.client.send_message(message.channel, random.choice(tweetList))
