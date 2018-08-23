import sys
sys.path.append('..')
from module import Module

import json
import random
import re
import requests

class Lights(Module):
	docs = {
		'description': 'Posts random Lights quotes'
	}

	def get_screenshots(self):
		return self.load_data('screenshots', static=True, default='[]')

	docs_lights_add = {
		'description': 'Adds a new Lights screenshot to the list',
		'usage': 'lights_add <link>'
	}
	async def cmd_lights_add(self, message, args, kwargs):
		if len(args) != 1:
			await self.send_error(message)
			return

		if not re.match('https://i\.imgur\.com/[A-Za-z0-9]+\.(png|jpg)/?', args[0]):
			await self.send_error(message, comment='link must be an Imgur direct link')
			return

		screenshots = self.get_screenshots()

		if args[0] in screenshots:
			await self.send_error(message, comment='link already exists in database')
			return

		screenshots.append(args[0])
		self.save_data('screenshots', screenshots, static=True)
		await self.send_success(message)

	docs_lights = {
		'description': 'Posts a random Lights quote'
	}
	async def cmd_lights(self, message, args, kwargs):
		screenshots = self.get_screenshots()

		if len(screenshots) == 0:
			await self.send_error(message, 'Lights database is empty')
		else:
			await message.channel.send(random.choice(screenshots))
