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

	docs_8ball = {
		'description': 'Gives a certified correct answer to your question'
	}
	async def cmd_8ball(self, message, args, kwargs):
		responses = [ "It is certain.", "It is decidedly so.", "Without a doubt.", "Yes, definitely.",
						"You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.",
						"Signs point to yes.", "Reply hazy try again.", "Ask again later.", "Better not tell you now.",
						"Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
						"My sources say no.", "Outlook not so good.", "Very doubtful." ]
		await self.client.send_message(message.channel, message.author.mention + " :8ball: " + random.choice(responses))
