import sys
sys.path.append('..')
from module import Module

import random
import requests
import re
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

	docs_tedcruz = {
		'description': 'Posts a random tweet from @commentiquette to @tedcruz'
	}
	async def cmd_tedcruz(self, message, args, kwargs):
		tweets = set(self.load_data('tedcruz', default='[]'))

		# this uses an ancient, non-Javascript mobile version of Twitter
		page = requests.get('https://mobile.twitter.com/search?q=ted%20OR%20cruz%20OR%20tedcruz%20from%3Acommentiquette').text

		while page:
			links = { 'https://twitter.com' + link for link in re.findall('/commentiquette/status/\d+', page) }
			found_existing_link = any([ link in tweets for link in links ])
			tweets = tweets.union(links)

			next_link_match = re.search('<a href="(.+)"> Load older Tweets </a>', page)

			if next_link_match and not found_existing_link:
				next_link = 'https://mobile.twitter.com' + next_link_match.group(1)
				page = requests.get(next_link).text
			else:
				page = None

		await message.channel.send(random.choice(list(tweets)))
		self.save_data('tedcruz', list(tweets))
