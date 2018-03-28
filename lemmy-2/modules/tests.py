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

	docs_channel_type = {
		'description': 'Returns the type of the active channel'
	}
	async def cmd_channel_type(self, message, args, kwargs):
		await self.client.send_message(message.channel, type(message.channel))

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

	async def cmd_chunk_text(self, message, args, kwargs):
		text = '''On May 14, 2000, marchers descended upon Washington, D.C., from all corners of the country. On a bright spring day, an estimated seven hundred and fifty thousand people listened to a series of speakers, some of whom had lost friends and family members to gun violence, engage in a collective call for tougher gun laws. The protesters’ sheer numbers and the power of their message were such that it seemed nobody would dare defy them.

That was the Million Mom March. It followed a series of horrendous mass shootings, including the massacre at Columbine High School. And it was followed by almost two decades of inaction on Congress’s part. “Today, the year 2000 is remembered not for the birth of a gun control movement,” USA Today’s Rick Hampson noted last week, “but for the start of the National Rifle Association’s two-decade domination of gun politics.”

Will the aftermath of this weekend’s March for Our Lives be any different? It’s hard to know the difference between the cynical argument and the realist one. The White House, both houses of Congress, and most state legislatures and governor’s mansions are under the control of the Republican Party, which remains firmly in hock to the gun lobby. Right after the Parkland shooting, Donald Trump promised to stand up to the N.R.A., and then caved almost immediately. The country is in a feverish state. The news agenda changes by the hour, and even huge events, such as this Saturday’s giant marches in Washington and other cities, tend to fade from the headlines quickly.

But there are grounds for optimism. First, the marches on Saturday were unprecedented not just in numbers—far more than a million people participated around the country—but also in geographic spread. Take upstate New York, which is normally considered a pro-gun area. Roughly five thousand people marched in Rochester, the biggest gun-control demonstration the city has ever seen. Another three thousand marched in Buffalo, and more than a thousand marched in Syracuse. There were also demonstrations in many smaller towns, such as Batavia, Oneonta, and Cobleskill. Poughkeepsie saw some eight thousand protesters.

“I think that marches alone are not going to sway votes in Congress, but they are an indication of a lot of momentum all around the state,” Rebecca Fischer, the executive director of New Yorkers Against Gun Violence, told me on Monday. “We have been building towards this moment since Sandy Hook. The silent majority is no longer silent.”

A second key point is that the Never Again movement is led by a group of schoolkids who have experienced the reality of gun violence firsthand. In the aftermath of Sandy Hook, President Obama became the public face of the gun-control movement as he tried to cajole Congress into acting. The Republicans and the N.R.A. adopted their usual hyper-partisan tactics, which succeeded in blocking any legislation. Today, though, the gun lobby is confronted with a group of articulate and nonpartisan teen-agers, whose presence gives their rallies tremendous emotional power and also insures blanket media coverage.

The Republicans are discombobulated. On his Facebook page, the Iowa congressman Steve King attacked Emma González, one of the memorable speakers at Saturday’s march in Washington, mocking her Cuban heritage and suggesting that she was an apologist for the Castro regime. Rick Santorum, a former G.O.P. Presidential candidate, said that schoolkids should learn how to administer C.P.R. rather than calling for stronger gun laws.

Support for stricter gun laws always spikes after mass shootings. In this case, though, the response has been stronger than usual. In a widely cited Quinnipiac University poll, ninety-seven per cent of Republicans said that they supported background checks for all gun buyers, seventy-seven per cent said that they supported mandatory waiting periods for all gun purchases, and forty-three per cent said that they supported a ban on assault weapons. To be sure, that survey was taken immediately after the shooting. But a newer Quinnipiac survey, taken last week, found that forty-one per cent of Republicans “think Congress needs to do more to reduce gun violence.”

Harsh experience has taught gun-control activists to be wary of poll findings. In actual elections, there are precious few examples of politicians, particularly Republicans, being voted out of office for failing to support tougher gun laws. But that’s why it was so encouraging to see an N.R.A. stalwart like Rick Scott, the Republican governor of Florida, break ranks and support raising the legal age for purchasing certain types of weapons in his state. Scott has at least one eye on running for the U.S. Senate. His about-face indicates that, in at least one Republican-run state, supporting moderate gun-control reforms is now a safer option than repeating the N.R.A. mantra of “No, No, No.”

As I noted last week, the shifting political climate is also reflected in increased support for gun-violence restraining orders—known as risk-protection orders—which enable judges to authorize the removal of guns from people who have exhibited threatening behavior. As part of a bill that Scott signed, Florida just adopted the use of these orders. Other states are moving in the same direction. In Albany, for example, gun-control activists and Democratic legislators are pushing Governor Andrew Cuomo to attach a risk-protection-order provision to the budget, which is supposed to be agreed upon by April 1st.

The final factor favoring change is the national political timetable. There is an election coming up, one in which the Republicans are already in serious trouble. To get majority support in Congress for stricter laws, the resurgent gun-control movement doesn’t need to create a political wave. Trump has already done that. It needs to ride the anti-Trump wave, and guide it in a certain direction.

That suddenly seems possible, although there will be disagreements about how far reforms should go. (The Parkland students are calling for a ban on assault weapons, which is sorely needed. Some Democrats in rural areas and Southern states would balk at supporting such a ban.) Moreover, the gun lobby should never be underestimated. After gun massacres, its strategy is always to hunker down and delay any reforms, secure in the knowledge that the typical supporter of stricter gun control will forget about the issue—or, at least, relegate it to just another issue to care about—before the typical N.R.A. member will.

This could happen again, of course. In an effort to whip up the rank and file, the gun lobby is sure to seize on a call to repeal the Second Amendment from John Paul Stevens, the retired Supreme Court Justice. But in the run-up to the midterms the Never Again movement will also be organizing more protests, beginning with another school walkout next month, on the anniversary of the Columbine shootings. Ultimately, it is up to everybody who cares about gun violence to stay engaged, and to heed the words of Rebecca Schneid, a sixteen-year-old Parkland survivor: “We understand that this is a marathon and that we’ll be fighting for years. We’re just getting started. Now we have to use our rights as voters to make things change.”'''
		for chunk in self.lemmy.chunk_text(text, chunk_prefix='```\n', chunk_suffix='\n```'):
			await self.client.send_message(message.channel, len(chunk))
