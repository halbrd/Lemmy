from module import Module

import discord
import datetime
import json

class Tests(Module):
	docs = {
		'description': 'Tests features of lemmy-2'
	}

	docs_send_error = {
		'description': 'Simulates an error occurring',
		'usage': 'send_error <message>',
		'examples': [ 'send_error', 'send_error \'This is what you did wrong!\'' ]
	}
	async def cmd_send_error(self, message, args, kwargs):
		raise Module.CommandError(args[0] if args else None)

	docs_send_success = {
		'description': 'Simulates an action successfully completing'
	}
	async def cmd_send_success(self, message, args, kwargs):
		raise Module.CommandSuccess(args[0] if args else None)

	docs_send_dm = {
		'description': 'Sends a direct message',
		'usage': 'send_dm direct_message <public_message>',
		'examples': [ 'send_error \'This message only goes to the recipient!\'', 'send_error \'This message goes to the command caller\' \'This message goes to the channel\'' ]
	}
	async def cmd_send_dm(self, message, args, kwargs):
		if len(args) == 0:
			raise Module.CommandDM
		elif len(args) == 1:
			raise Module.CommandDM(args[0])
		else:
			raise Module.CommandDM(args[0], args[1])

	docs_dump_args = {
		'description': 'Returns the args and kwargs parsed from the message',
		'usage': 'dump_args <args> <kwargs>',
		'examples': [ 'dump_args a d=1 b e=2 c f=3' ]
	}
	async def cmd_dump_args(self, message, args, kwargs):
		await self.client.send_message(message.channel, f'args:\n{str(args)}\nkwargs:\n{str(kwargs)}')

	async def cmd_no_docs(self, message, args, kwargs):
		await self.client.send_message(message.channel, 'This command has no docs to test the help text')

	async def cmd_embed_example(self, message, args, kwargs):
		embed_data = {
			'footer': {
				'text': 'Footer text',
				'icon_url': 'http://lynq.me/lemmy/emotes/BestState.png'
			},
			'image': { 'url': 'http://lynq.me/lemmy/emotes/DISCassidy.png' },
			'thumbnail': { 'url': 'http://lynq.me/lemmy/emotes/RikCreepy.png' },
			'author': {
				'name': 'Author name',
				'url': 'https://halbrd.com',
				'icon_url': 'http://lynq.me/lemmy/emotes/Tooth.png'
			},
			'fields': [
				{ 'inline': True, 'name': 'Field 1 (inline)', 'value': 'Field 1 value' },
				{ 'inline': True, 'name': 'Field 2 (inline)', 'value': 'Field 2 value' },
				{ 'inline': False, 'name': 'Field 3 (not inline)', 'value': 'Field 3 value' }
			],
			'color': 16030530,
			'timestamp': str(datetime.datetime.now()),
			'type': 'rich',
			'description': '# Header\nNormal text\n* Bullet point\n[Link text](http://halbrd.com)',
			'url': 'http://lynq.me/lemmy',
			'title': 'Title',
		}


		embed = discord.Embed()
		embed.title = embed_data['title']
		embed.type = embed_data['type']
		embed.description = embed_data['description']
		embed.url = embed_data['url']
		embed.timestamp = datetime.datetime.now()
		embed.colour = embed_data['color']
		embed.set_footer(text=embed_data['footer']['text'], icon_url=embed_data['footer']['icon_url'])
		embed.set_image(url=embed_data['image']['url'])
		embed.set_thumbnail(url=embed_data['thumbnail']['url'])
		embed.set_author(name=embed_data['author']['name'], url=embed_data['author']['url'], icon_url=embed_data['author']['icon_url'])
		for field in embed_data['fields']:
			embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])

		await self.client.send_message(message.channel, f'```json\n{json.dumps(embed_data, sort_keys=True, indent=2)}\n```', embed=embed)

	async def cmd_print_raw(self, message, args, kwargs):
		await self.client.send_message(message.channel, '```\n' + message.content + '\n```')
