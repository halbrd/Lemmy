import sys
sys.path.append('modules')
sys.path.append('modules/core')

# Lemmy's stuff
import LemmyUtils as Lutils
import LemmyCommands as Lcmds
import LemmyResources as Lres
import LemmyConstants as Lconst
import LemmyTags as Ltags
import LemmyRadio as Lradio
import LemmyConfig as Lconf
from LemmyRadio import LemmyRadio
from FloodProtector import FloodProtector
from CallLogger import CallLogger

# Other stuff
import discord
import asyncio
import datetime
import codecs
import shlex
import os
import re
from PIL import Image
import random
import logging

class LemmyBot:
	def __init__(self, token):
		if not discord.opus.is_loaded():
			discord.opus.load_opus('libopus-0.dll')

		### Load major member variables ###
		self.res = Lres.LemmyResources()
		self.tags = Ltags.LemmyTags()
		self.constants = Lconst.LemmyConstants()
		self.callLogger = None
		self.radio = Lradio.LemmyRadio(None, None)
		self.config = Lconf.LemmyConfig()
		self.floodProtectors = {
			"emote": FloodProtector(self.config.cooldown["emote"])
		}
		self.clientId = Lutils.GetConfigAttribute("global", "clientId")
		self.customCommands = Lutils.GetConfig("customcommands")

		self.client = discord.Client()

		print(Lutils.TitleBox("Registering Events"))

		@self.client.event
		async def on_message(msg):
			await Lutils.LogMessage(msg)

			# Message is a command
			if msg.content.startswith(self.config.symbol[(msg.server.id if msg.server is not None else None)]) and msg.author != self.client.user:
				dmsg = Lutils.ParseMessage(msg.content[len(self.config.symbol[(msg.server.id if msg.server is not None else None)]):])

				if dmsg.command is not None:
					if dmsg.command in self.config.command and self.config.command[dmsg.command]["enabled"]:
						if self.config.command[dmsg.command]["moderator"] and not Lutils.IsModOrAbove(msg.author):
							await self.client.send_message(msg.channel, self.constants.error + " " + self.constants.errNotMod)
						else:
							await self.config.command[dmsg.command]["function"](self, msg, dmsg)
					# Message is a custom command
					elif dmsg.command in self.customCommands:
						await self.client.send_message(msg.channel, self.customCommands[dmsg.command])
						"""def replaceDefaults(string):
							for match in re.findall("{.+}", string):
								del string[match.end]
								del string[match.start]

						responseTemplate = self.customCommands[dmsg.command]
						requiredParamCount = response.count("{}")
						totalParamCount = len(re.findall("{.*}", responseTemplate))
						suppliedParamCount = len(dmsg.params)
						if suppliedParamCount == totalParamCount:
							await self.client.send_message(msg.channel, responseTemplate.format(*dmsg.params))
						elif suppliedParamCount == requiredParamCount:


							await self.client.send_message(msg.channel, self.constants.error + " Incorrect number of arguments ({} total, {} mandatory, got {})".format(totalParamCount, requiredParamCount, suppliedParamCount))
						else:
							await self.client.send_message(msg.channel, self.customCommands[dmsg.command])"""

			# Message is an emote
			elif msg.content in self.res.emotes and msg.author != self.client.user:
				if self.floodProtectors["emote"].Ready(msg.author.id):
					await Lutils.SendEmote(self.client, msg)
					self.floodProtectors["emote"].Sent(msg.author.id)
					Lutils.LogEmoteUse(self.res, msg.author, msg.content)
				else:
					await self.client.delete_message(msg)

			# Message is a sticker
			elif msg.content in self.res.stickers and msg.author != self.client.user:
				if self.floodProtectors["emote"].Ready(msg.author.id):
					await Lutils.SendSticker(self.client, msg)
					self.floodProtectors["emote"].Sent(msg.author.id)
					Lutils.LogEmoteUse(self.res, msg.author, msg.content)
				else:
					await self.client.delete_message(msg)

			# Message is a Skype emote
			elif re.match("\(" + self.res.skype.emoteMatch + "\)", msg.content):
				if self.floodProtectors["emote"].Ready(msg.author.id):
					await Lutils.SendSkypeEmote(self.client, msg)
					self.floodProtectors["emote"].Sent(msg.author.id)
					Lutils.LogEmoteUse(self.res, msg.author, msg.content[1:-1])
				else:
					await self.client.delete_message(msg)

			# Message is a Skype flag
			elif re.match("\(flag:" + self.res.skype.flagMatch + "\)", msg.content):
				if self.floodProtectors["emote"].Ready(msg.author.id):
					await Lutils.SendSkypeFlag(self.client, msg)
					self.floodProtectors["emote"].Sent(msg.author.id)
					Lutils.LogEmoteUse(self.res, msg.author, msg.content[1:-1])
				else:
					await self.client.delete_message(msg)

			else:
				imageMatch = "(" + "|".join(self.res.emotes) + "|" + "|".join(self.res.stickers) + ")"

				# Message is a hybrid emote
				if re.match(imageMatch + "( +" + imageMatch + ")+", msg.content):
					imageTerms = msg.content.split()
					images = []
					for imageTerm in imageTerms:
						if imageTerm in self.res.emotes:
							images.append(Image.open("pics/emotes/" + imageTerm + ".png"))
						elif imageTerm in self.res.stickers:
							images.append(Image.open("pics/stickers/" + imageTerm + ".png"))
						else:
							images.append(Image.new("RGBA", (64,64)))

					# This saves the combined image as pics/temp.png
					Lutils.CombineImages(images)

					await Lutils.SendTemp(self.client, msg)

					for image in imageTerms:
						Lutils.LogEmoteUse(self.res, msg.author, image)

			tagMatch = "(" + "|".join([x for x in self.tags.db]) + ")"

			# Ampersand-prefixed tags
			for match in re.findall("&" + tagMatch, msg.content):
				await self.client.send_message(msg.channel, Lutils.GetPingText(self, msg, match))
				await self.client.send_message(msg.channel, "Note: !james is deprecated, and has been replaced with native Discord roles and the !role command. Use @tag to ping a tag.")


		@self.client.event
		async def on_ready():
			print("Successfully logged in.")
			print("NAME: " + self.client.user.name)

			print(Lutils.TitleBox("Checking Command Symbols"))
			for server in self.client.servers:
				if server.id in self.config.symbol:
					print("Server '" + server.name + "' has been assigned the command symbol '" + self.config.symbol[server.id] + "'.")
				else:
					print("Warning! Server '" + server.name + "' has no command symbol assigned to it.")

			print(Lutils.TitleBox("Checking Channel Mapping"))
			warnings = False

			print("Voice to text channel map loaded with " + str(len(self.config.voiceToText)) + " servers mapped.")
			print("Text to voice channel map loaded with " + str(len(self.config.textToVoice)) + " servers mapped.")

			for server in self.client.servers:

				# Server hasn't been mapped at all
				if server.id not in self.config.voiceToText and server.id not in self.config.textToVoice:
					print("Warning! Server '" + server.name + "' does not have its voice or text channels mapped.")
					warnings = True

				# Server has had text channels mapped, but not voice channels
				elif server.id not in self.config.voiceToText:
					print("Warning! Server '" + server.name + "' does not have its voice channels mapped.")
					warnings = True
					for channel in server.channels:
						if channel.type == discord.ChannelType.text and channel.id not in self.config.textToVoice[server.id]:
							print("  Warning! Server '" + server.name + "'s text channel " + channel.name + " has not been mapped to a voice channel (or None).")

				# Server has had voice channels mapped, but not text channels
				elif server.id not in self.config.textToVoice:
					print("Warning! Server '" + server.name + "' does not have its text channels mapped.")
					warnings = True
					for channel in server.channels:
						if channel.type == discord.ChannelType.voice and channel.id not in self.config.voiceToText[server.id]:
							print("  Warning! Server '" + server.name + "'s voice channel " + Lutils.StripUnicode(channel.name).strip() + " has not been mapped to a text channel (or None).")

				# Server has had voice and text channels mapped
				else:
					print("Server '" + server.name + "' has its voice and text channels mapped.")
					for channel in server.channels:
						if channel.type == discord.ChannelType.text and channel.id not in self.config.textToVoice[server.id]:
							print("Warning! Server '" + server.name + "'s text channel " + channel.name + " has not been mapped to a voice channel (or None).")
							warnings = True
					for channel in server.channels:
						if channel.type == discord.ChannelType.voice and channel.id not in self.config.voiceToText[server.id]:
							print("Warning! Server '" + server.name + "'s voice channel " + Lutils.StripUnicode(channel.name).strip() + " has not been mapped to a text channel (or None).")
							warnings = True

			if not warnings:
				print("All channels of all servers have been mapped.")


			print(Lutils.TitleBox("Registering New Users"))
			members = []
			for server in self.client.servers:
				for member in server.members:
					members.append(member)

			cursor = self.res.sqlConnection.cursor()

			for member in members:
				cursor.execute("SELECT * FROM tblUser WHERE UserId = ?", (member.id,))
				if len(cursor.fetchall()) == 0:
					print("Registering new user '" + member.name + "'.")
					cursor.execute("INSERT INTO tblUser VALUES (?, 10)", (member.id,))
				self.res.sqlConnection.commit()

			print(Lutils.TitleBox("Initializing Call Logger"))
			channelList = []
			for server in self.client.servers:
				for channel in server.channels:
					if channel.type == discord.ChannelType.voice:
						channelList.append(channel)
			self.callLogger = CallLogger(channelList)
			print("Call Logger initialized with the following channels:")
			for channel in channelList:
				print("[" + Lutils.StripUnicode(channel.server.name) + "] " + Lutils.StripUnicode(channel.name.strip()))

			# print(Lutils.TitleBox("Sending Online Message"))

			# channelList = []
			# for server in self.client.servers:
			# 	for channel in server.channels:
			# 		channelList.append(channel)

			# for server in self.client.servers:
			# 	words = []
			# 	for channel in server.channels:
			# 		logs = self.client.logs_from(channel, limit=10)
			# 		async for message in logs:
			# 			if message.content:
			# 				words = words + message.content.split()

			# 	sentence = ""
			# 	for _ in range(random.randint(5, 15)):
			# 		sentence += random.choice(words) + " "
			# 	sentence += "."

			# 	await self.client.send_message(server.default_channel, "A great person once said, " + sentence)

			await self.client.change_status(game=discord.Game(name="!help for info"))

			logging.getLogger("discord.gateway").setLevel(logging.CRITICAL)

			print(Lutils.TitleBox("Listening For Messages"))


		@self.client.event
		async def on_message_edit(before, after):
			if before.content != after.content:
				await Lutils.LogMessageEdit(before, after)

		@self.client.event
		async def on_message_delete(msg):
			await Lutils.LogMessageDelete(msg)

		@self.client.event
		async def on_voice_state_update(before, after):
			channelList = []
			for server in self.client.servers:
				for channel in server.channels:
					if channel.type == discord.ChannelType.voice:
						channelList.append(channel)
			responses = self.callLogger.UpdateStatuses(channelList)

			for response in responses:
				channel = response[0]
				timeString = response[1]

				if channel.server.id in self.config.voiceToText:
					textChannelId = self.config.voiceToText[channel.server.id][channel.id]
					if textChannelId is not None:
						textChannel = discord.utils.find(lambda m: m.id == textChannelId, channel.server.channels)
						if not timeString.startswith("00:00:"):
							await self.client.send_message(textChannel if textChannel is not None else channel.server.get_default_channel(), "Call ended in " + Lutils.StripUnicode(channel.name).strip() + ", duration " + timeString)

		print(Lutils.TitleBox("Logging Into Discord"))

		print("Attempting to log in.")
		try:
			self.client.run(token)
		except Exception as e:
			print("ERROR logging into Discord! (" + str(e) + ")")
			input("Press enter to exit.\n")
			quit()
