import sys
sys.path.append('..')
from module import Module

import random

class Extras(Module):
	docs = {
		'description': 'Provides non-essential functions'
	}

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

	docs_choose = {
		'description': 'Chooses between the given options',
		'usage': 'choose <option> or <option> or ...',
		'examples': [ 'choose go left or go right or stay still' ]
	}
	async def cmd_choose(self, message, args, kwargs):
		params = [ 'OR' if arg.lower() == 'or' else arg for arg in args ]
		options = ' '.join(params).split(' OR ')
		options = [ option for option in options if option != '' ]

		if len(options) == 1:
			await self.client.send_message(message.channel, message.author.mention + '   I can\'t decide!')
		elif len(options) > 0:
			await self.client.send_message(message.channel, message.author.mention + f'   `{random.choice(options)}`')
		else:
			await self.send_error(message)
			return
