import sys
sys.path.append('..')
from module import Module

import os
import random
import discord
import json
import requests
from bs4 import BeautifulSoup
from itertools import zip_longest

class Memes(Module):
	docs = {
		'description': 'Commands that serve no purpose whatsoever'
	}

	docs_ruseman = {
		'description': 'Posts a random ruseman'
	}
	async def cmd_ruseman(self, message, args, kwargs):
		image_location = 'data/Memes/rusemans/'
		await self.client.send_file(message.channel, image_location + random.choice(os.listdir(image_location)))

	docs_genjimain = {
		'description': 'Posts a random Genji main'
	}
	async def cmd_genjimain(self, message, args, kwargs):
		genji_mains = self.load_data('genjimain')['links']
		await self.client.send_message(message.channel, random.choice(genji_mains))
