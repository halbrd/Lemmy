import sys
sys.path.append('..')
from module import Module

import discord
import datetime

class CallLogger(Module):
	docs = {
		'description': 'Logs information about voice channel calls'
	}

	def sanitize_channel_name(name):
		return name.encode('ascii', 'ignore').decode('ascii').strip()

	def format_duration(timedelta):
		seconds = timedelta.seconds
		return '{}:{:02}:{:02}'.format(seconds // 3600, seconds % 3600 // 60, seconds % 60)

	def __init__(self, lemmy):
		Module.__init__(self, lemmy)

		self.channel_map = self.load_data('channelmap')
		self.calls = {}

	async def on_ready(self):
		await self.handle_voice_state_update()

	def get_channel_populations(self):
		voice_channels = [
			channel
			for server in self.client.guilds
			for channel in server.channels
			if channel.type == discord.ChannelType.voice
		]

		return {
			str(channel.id): len(channel.members)
			for channel in voice_channels
		}

	def get_channel_by_id(self, id):
		return discord.utils.find(
			lambda channel: str(channel.id) == str(id),
			self.client.get_all_channels(),
		)

	async def send_call_end_notification(self, text_channel, voice_channel, duration):
		await text_channel.send(embed=discord.Embed(
			title=f'Call ended in **{CallLogger.sanitize_channel_name(voice_channel.name)}**',
			description='🎙️ ' + CallLogger.format_duration(duration),
		))


	async def on_voice_state_update(self, member, before, after):
		await self.handle_voice_state_update()

	async def handle_voice_state_update(self):
		channel_populations = self.get_channel_populations()
		responses = []

		# update call store and collect responses
		for voice_id, population in channel_populations.items():
			# ensure that the channel is in the call store
			if not voice_id in self.calls.keys():
				self.calls[voice_id] = None


			was_call = not self.calls[voice_id] is None
			is_call = population > 1

			if not was_call and is_call:
				self.calls[voice_id] = datetime.datetime.now()
			elif was_call and not is_call:
				# only log the call if it was at least a minute
				duration = datetime.datetime.now() - self.calls[voice_id]
				if duration.seconds >= 60:
					responses.append((voice_id, duration))

				# always clear the call from the store
				self.calls[voice_id] = None

		# send responses
		for voice_id, duration in responses:
			# ignore if there isn't a text channel associated with the voice channel
			if not voice_id in self.channel_map.keys():
				continue

			voice_channel = self.get_channel_by_id(voice_id)
			text_channel = self.get_channel_by_id(self.channel_map[voice_id])

			await self.send_call_end_notification(text_channel, voice_channel, duration)

		# prevent memory leak from channels that get deleted
		self.calls = { k: v for k, v in self.calls.items() if v is not None }
