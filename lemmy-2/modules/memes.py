import sys
sys.path.append('..')
from module import Module

import random

class Memes(Module):
	docs = {
		'description': 'Commands that serve no purpose whatsoever'
	}

	docs_ruseman = {
		'description': 'Posts a random ruseman'
	}
	async def cmd_ruseman(self, message, args, kwargs):
		rusemans = self.load_data('ruseman', static=True)['links']
		await message.channel.send(random.choice(rusemans))

	docs_genjimain = {
		'description': 'Posts a random Genji main'
	}
	async def cmd_genjimain(self, message, args, kwargs):
		genji_mains = self.load_data('genjimain', static=True)['links']
		await message.channel.send(random.choice(genji_mains))
