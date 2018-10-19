import sys
sys.path.append('..')
from module import Module

import discord
import datetime

# TODO: lookup external entities by ID

class Info(Module):
	docs = {
		'description': 'Provides information about a Discord entity'
	}

	docs_serverinfo = {
		'description': 'Provides information about the current server'
	}
	async def cmd_server_info(self, message, args, kwargs):
		server = message.channel.guild
		embed = discord.Embed()

		# name
		embed.title = server.name
		# splash url
		if server.splash_url:
			embed.url = server.splash_url
		# member count and server size
		embed.add_field(name=f'{server.member_count} members', value='Large-sized server' if server.large else 'Standard-sized server', inline=True)
		# roles
		role_counts = {}
		for member in server.members:
			for role in member.roles:
				role_counts[role.name] = role_counts.get(role.name, 0) + 1
		sorted_roles = sorted(role_counts, key=role_counts.get, reverse=True)
		embed.add_field(name=f'{len(server.roles)} roles', value=f'Top roles: {", ".join(sorted_roles[1:min([4, len(sorted_roles)])])}', inline=True)
		# emojis
		embed.add_field(name=f'{len(server.emojis)} emojis',
		  value=f'{len(list(filter(lambda emoji: not emoji.animated, server.emojis)))} static, {len(list(filter(lambda emoji: emoji.animated, server.emojis)))} animated', inline=True)
		# region
		embed.add_field(name='Voice region', value=server.region, inline=True)
		# afk voice channel
		embed.add_field(name='AFK voice channel', value=f'{server.afk_channel.name} ({server.afk_timeout // 60} mins)', inline=True)
		# system channel
		embed.add_field(name='System channel', value='#' + server.system_channel.name, inline=True)
		# verification/mfa level
		# note: the __str__ call on the following line is NOT redundant, due to how the enum resolves
		embed.add_field(name=f'Verification level: {str(server.verification_level)}', value=f'MFA {"not " if server.mfa_level == 0 else ""}required', inline=True)
		# content filter
		embed.add_field(name=f'Content filter', value=server.explicit_content_filter, inline=True)
		# owner
		embed.add_field(name=f'Current owner', value=f'@{server.owner.nick or server.owner.name}', inline=True)
		# splash
		if server.splash:
			embed.add_field(name=f'Splash', value=server.splash, inline=True)
		# special features
		if server.features:
			embed.add_field(name='Special Features', value=server.features, inline=True)
		# server icon
		embed.set_image(url=server.icon_url)
		# creator
		embed.set_footer(text=f'Created by @{server.owner.nick or server.owner.name}', icon_url=server.owner.avatar_url)
		# created at
		embed.timestamp = server.created_at

		await message.channel.send(embed=embed)

	def resolve_member(server, term):
		try_attrs = [ 'id', 'mention', 'nick', 'name' ]

		for attr in try_attrs:
			user = discord.utils.find(lambda user: str(getattr(user, attr)).lower() == term.lower(), server.members)
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
	async def cmd_user_info(self, message, args, kwargs):
		if len(args) > 1:
			await self.send_error(message)
			return

		if len(args) == 0:
			user = message.author
		elif len(args) == 1:
			search_term = args[0]
			user = Info.resolve_member(message.guild, search_term)

			if not user:
				await self.send_error(message, comment=f'Couldn\'t find a user that matched \'{search_term}\'')
				return

		embed = discord.Embed()

		# username, discriminator, nickname, default avatar
		embed.set_author(name=f'{user.name}#{user.discriminator}' + (f' ({user.nick})' if user.nick else '') + (' [🤖]' if user.bot else ''), icon_url=user.default_avatar_url)
		# online status
		status_colors = {
			'online': discord.Color.green(),
			'idle': discord.Color.gold(),
			'dnd': discord.Color.red(),
			'offline': discord.Color.light_grey()
		}
		if str(user.status) in status_colors:
			embed.color = status_colors[str(user.status)]
		# top role
		embed.add_field(name='Top role', value=user.top_role.name)
		# joined server at
		joined_at_aest = user.joined_at.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
		embed.add_field(name=f'Joined {message.guild.name}', value=f'{joined_at_aest:%B %d, %Y - %H:%M}')
		# avatar
		embed.set_image(url=user.avatar_url)
		# joined Discord at
		embed.set_footer(text=f'Joined Discord:')
		embed.timestamp = user.created_at

		await message.channel.send(embed=embed)
