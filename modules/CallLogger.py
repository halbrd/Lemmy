import datetime
import discord

class CallLogger:
	def __init__(self, channels):
		self.db = {}
		for channel in channels:
			if channel.type == "voice":
				self.db[channel.id] = None

	def UpdateStatuses(self, channels):
		responses = []

		for channel in channels:
			if channel.type == discord.ChannelType.voice:
				if not channel.id in self.db:
					self.db[channel.id] = None
				else:
					# If there wasn't 2 people before and isn't now
					if self.db[channel.id] is None and len(channel.voice_members) < 2:
						continue
					# If there wasn't 2 people before and there is now
					elif self.db[channel.id] is None and len(channel.voice_members) >= 2:
						self.db[channel.id] = datetime.datetime.now()
					# If there was 2 people before and still is
					elif self.db[channel.id] is not None and len(channel.voice_members) >= 2:
						continue
					# If there was 2 people before and isn't now
					elif self.db[channel.id] is not None and len(channel.voice_members) < 2:
						callLength = datetime.datetime.now() - self.db[channel.id]
						self.db[channel.id] = None
						seconds = callLength.seconds
						prettyString = '{:02}:{:02}:{:02}'.format(seconds // 3600, seconds % 3600 // 60, seconds % 60)
						responses.append([channel, prettyString])

		return responses