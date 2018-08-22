import sys
sys.path.append('..')
from module import Module

import discord

class Info(Module):
	docs = {
		'description': 'Provides information about a Discord entity'
	}

	docs_serverinfo = {
		'description': 'Provides information about the current server'
	}
	async def cmd_serverinfo(self, message, args, kwargs):
		server = message.channel.server
		embed = discord.Embed()

		embed.title = server.name
		if server.splash_url:
			embed.url = server.splash_url
		embed.add_field(name=f'{server.member_count} members', value='Large server' if server.large else 'Standard server', inline=True)
		embed.add_field(name='Region', value=server.region, inline=True)
		embed.add_field(name='Unique ID', value=server.id, inline=True)
		embed.add_field(name='AFK channel', value=f'{server.afk_channel.name} ({server.afk_timeout // 60} minutes)', inline=True)
		embed.add_field(name=f'Verification level: {server.verification_level}', value=f'MFA level: {server.mfa_level}', inline=True)
		embed.add_field(name='Special Features', value=server.features if server.features else 'None', inline=True)
		role_counts = {}
		for member in server.members:
			for role in member.roles:
				role_counts[role.name] = role_counts.get(role.name, 0) + 1
		sorted_roles = sorted(role_counts, key=role_counts.get, reverse=True)
		embed.add_field(name=f'{len(server.roles)} roles', value=f'Top role: {", ".join(sorted_roles[1])}', inline=True)
		embed.set_image(url=server.icon_url)
		embed.set_footer(text=f'Created by @{server.owner.name}', icon_url=server.owner.avatar_url)
		embed.timestamp = server.created_at

		await self.client.send_message(message.channel, embed=embed)

'''
[Given]
	name
	icon_url

[Interesting]
	region
	id
	owner
	afk_channel/timeout
	large
	verification_level
	mfa_level
	default_channel
	member_count
	created_at
	features

[Eh]
	roles
	emojis
'''
