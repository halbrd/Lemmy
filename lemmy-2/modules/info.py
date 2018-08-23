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

		embed.title = 'Server info: ' + server.name
		if server.splash_url:
			embed.url = server.splash_url
		embed.add_field(name=f'{server.member_count} members', value='Large server' if server.large else 'Standard server', inline=True)
		embed.add_field(name='Region', value=server.region, inline=True)
		embed.add_field(name='Unique ID', value=server.id, inline=True)
		embed.add_field(name='AFK voice channel', value=f'{server.afk_channel.name} ({server.afk_timeout // 60} mins)', inline=True)
		embed.add_field(name='Default channel', value='#' + server.default_channel.name, inline=True)
		embed.add_field(name=f'Verification level: {server.verification_level}', value=f'MFA level: {server.mfa_level}', inline=True)
		embed.add_field(name='Special Features', value=server.features if server.features else 'None', inline=True)
		role_counts = {}
		for member in server.members:
			for role in member.roles:
				role_counts[role.name] = role_counts.get(role.name, 0) + 1
		sorted_roles = sorted(role_counts, key=role_counts.get, reverse=True)
		embed.add_field(name=f'{len(server.roles)} roles', value=f'Top roles: {", ".join(sorted_roles[1:4])}', inline=True)
		# embed.add_field(name=f'{len(server.emojis)} emojis',   TODO: blocked by 1.0 migration
		#   value=f'{len(list(filter(lambda emoji: emoji.animated, server.emojis)))} animated')
		embed.set_image(url=server.icon_url)
		embed.set_footer(text=f'Created by @{server.owner.name}', icon_url=server.owner.avatar_url)
		embed.timestamp = server.created_at

		await self.client.send_message(message.channel, embed=embed)

	def resolve_member(server, term):
		try_attrs = [ 'id', 'mention', 'nick', 'name' ]

		for attr in try_attrs:
			user = discord.utils.find(lambda user: getattr(user, attr) == term, server.members)
			if user:
				return user

		return None

	docs_userinfo = {
		'description': 'Provides information about a user',
		'usage': 'userinfo <id, username, or mention>',
		'examples': [
			'userinfo 174046218190716929',
			'userinfo Lemmy',
			'userinfo @Lemmy'
		]
	}
	async def cmd_userinfo(self, message, args, kwargs):
		if len(args) > 1:
			await self.send_error(message)
			return

		if len(args) == 0:
			user = message.author
		elif len(args) == 1:
			search_term = args[0]
			user = Info.resolve_user(message.server, search_term)

			if not user:
				await self.send_error(message, comment=f'Couldn\'t find a user that matched \'{search_term}\'')
				return

		embed = discord.Embed()

		embed.set_author(name=f'{user.name}#{user.discriminator}' + (f' ({user.nick})' if user.nick else ''), icon_url=user.default_avatar)   # TODO: status colors
		embed.set_image(url=user.avatar_url)
		embed.set_footer(text=f'Joined {user.server}:')
		embed.timestamp = user.created_at

		await self.client.send_message(message.channel, embed=embed)

	

'''
User

[Given]
	- name
	- avatar_url (handle null)
[Interesting]
	- id
	- discriminator
	- created_at
[Eh]
	- default_avatar
	- permissions_in
	- bot

Member
[Interesting]
	- voice
	- joined_at
	- status
	- game
	- nick
	- colour
	- top_role
[Eh]
	- server_permissions
'''



'''

Server

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
