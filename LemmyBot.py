import sys
sys.path.append('modules')

# Lemmy's stuff
import LemmyUtils as Lutils
import LemmyCommands as Lcmds
import LemmyResources as Lres
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

class LemmyBot:
	def __init__(self, username, password):
		if not discord.opus.is_loaded():
			discord.opus.load_opus('libopus-0.dll')

		self.res = Lres.LemmyResources()
		self.res.Load()

		self.help = Lcmds.help
		self.emotes = Lcmds.emotes
		self.stickers = Lcmds.stickers
		self.lenny = Lcmds.lenny
		self.refresh = Lcmds.refresh
		self.correct = Lcmds.correct
		self.eightball = Lcmds.eightball
		self.userinfo = Lcmds.userinfo
		self.channelinfo = Lcmds.channelinfo
		self.james = Lcmds.james
		self.happening = Lcmds.happening
		self.ruseman = Lcmds.ruseman
		self.lemmycoin = Lcmds.lemmycoin
		self.channelids = Lcmds.channelids
		self.serverinfo = Lcmds.serverinfo
		self.choose = Lcmds.choose
		#self.radio = Lcmds.radio
		#self.tts = Lcmds.tts
		self.logout = Lcmds.logout

		# Map of function names to their equivalent function pointers
		self.funcMap = {
			"help": self.help,
			"emotes": self.emotes,
			"stickers": self.stickers,
			"lenny": self.lenny,
			"refresh": self.refresh,
			"f5": self.refresh,
			"correct": self.correct,
			"8ball": self.eightball,
			"userinfo": self.userinfo,
			"channelinfo": self.channelinfo,
			"james": self.james,
			"happening": self.happening,
			"ruseman": self.ruseman,
			"lemmycoin": self.lemmycoin,
			"lc": self.lemmycoin,
			"l$": self.lemmycoin,
			"channelids": self.channelids,
			"serverinfo": self.serverinfo,
			"choose": self.choose,
			#"radio": self.radio,
			#"tts": self.tts,
			"logout": self.logout
		}
		
		self.symbolMap = {
			"77041788564545536": "!",   # Better Than Skype
			"77041897784225792": "!"   # blue87
		}

		self.floodProtectors = {
			"emote": FloodProtector(5),
			"sticker": FloodProtector(5)
		}

		self.callLogger = None

		self.client = discord.Client()

		print(Lutils.TitleBox("Registering Events"))

		@self.client.event
		async def on_ready():
			print("Successfully logged in.")
			print("USERNAME: " + username)
			print("PASSWORD: " + "".join(["*" for x in password]))

			print(Lutils.TitleBox("Checking Command Symbols"))
			for server in self.client.servers:
				if server.id in self.symbolMap:
					print("Server '" + server.name + "' has been assigned the command symbol '" + self.symbolMap[server.id] + "'.")
				else:
					print("Warning! Server '" + server.name + "' has no command symbol assigned to it.")

			print(Lutils.TitleBox("Checking Channel Mapping"))
			warnings = False
			for server in self.client.servers:

				# Server hasn't been mapped at all
				if server.id not in self.res.voiceToTextChannelMaps and server.id not in self.res.textToVoiceChannelMaps:
					print("Warning! Server '" + server.name + "' does not have its voice or text channels mapped.")
					warnings = True

				# Server has had text channels mapped, but not voice channels
				elif server.id not in self.res.voiceToTextChannelMaps:
					print("Warning! Server '" + server.name + "' does not have its voice channels mapped.")
					warnings = True
					for channel in server.channels:
						if channel.type == discord.ChannelType.text and channel.id not in self.res.textToVoiceChannelMaps[server.id]:
							print("  Warning! Server '" + server.name + "'s text channel " + channel.name + " has not been mapped to a voice channel (or None).")

				# Server has had voice channels mapped, but not text channels
				elif server.id not in self.res.textToVoiceChannelMaps:
					print("Warning! Server '" + server.name + "' does not have its text channels mapped.")
					warnings = True
					for channel in server.channels:
						if channel.type == discord.ChannelType.voice and channel.id not in self.res.voiceToTextChannelMaps[server.id]:
							print("  Warning! Server '" + server.name + "'s voice channel " + Lutils.StripUnicode(channel.name).strip() + " has not been mapped to a text channel (or None).")

				# Server has had voice and text channels mapped
				else:
					print("Server '" + server.name + "' has its voice and text channels mapped.")
					for channel in server.channels:
						if channel.type == discord.ChannelType.text and channel.id not in self.res.textToVoiceChannelMaps[server.id]:
							print("Warning! Server '" + server.name + "'s text channel " + channel.name + " has not been mapped to a voice channel (or None).")
							warnings = True
					for channel in server.channels:
						if channel.type == discord.ChannelType.voice and channel.id not in self.res.voiceToTextChannelMaps[server.id]:
							print("Warning! Server '" + server.name + "'s voice channel " + Lutils.StripUnicode(channel.name).strip() + " has not been mapped to a text channel (or None).")
							warnings = True

			if not warnings:
				print("All channels of all servers have been mapped.")


			print(Lutils.TitleBox("Registering Users"))
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

			print(Lutils.TitleBox("Listening For Messages"))


		@self.client.event
		async def on_message(msg):
			await Lutils.LogMessage(msg)

			# Message is a command
			if msg.content.startswith(self.symbolMap[msg.server.id]) and msg.author != self.client.user:
				dmsg = Lutils.ParseMessage(msg.content[len(self.symbolMap[msg.server.id]):])

				if dmsg.command in self.funcMap:
					await self.funcMap[dmsg.command](self, msg, dmsg)

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
				if self.floodProtectors["sticker"].Ready(msg.author.id):
					await Lutils.SendSticker(self.client, msg)
					self.floodProtectors["sticker"].Sent(msg.author.id)
					Lutils.LogEmoteUse(self.res, msg.author, msg.content)
				else:
					await self.client.delete_message(msg)

			else:
				imageMatch = "("
				imageMatch += "|".join(self.res.emotes)
				imageMatch += "|".join(self.res.stickers)
				imageMatch += ")"

				# Message is a hybrid emote
				if re.match(imageMatch + "( " + imageMatch + ")+", msg.content):
					imageTerms = msg.content.split()
					images = []
					for imageTerm in imageTerms:
						# I'm *really* sorry about these next 4 lines.
						try:
							images.append(Image.open("pics/emotes/" + imageTerm + ".png"))
						except IOError:
							images.append(Image.open("pics/stickers/" + imageTerm + ".png"))

					# This saves the combined image as pics/result.png
					Lutils.CombineImages(images)

					await self.client.send_message(msg.channel, "__**" + msg.author.name + "**__")
					await self.client.send_file(msg.channel, "pics/result.png")

					os.remove("pics/result.png")

					await self.client.delete_message(msg)

					for image in imageTerms:
						Lutils.LogEmoteUse(self.res, msg.author, image)
						

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

				if channel.server.id in self.res.voiceToTextChannelMaps:
					textChannelId = self.res.voiceToTextChannelMaps[channel.server.id][channel.id]
					if textChannelId is not None:
						textChannel = discord.utils.find(lambda m: m.id == textChannelId, channel.server.channels)
						await self.client.send_message(textChannel if textChannel is not None else channel.server.get_default_channel(), "Call ended in " + Lutils.StripUnicode(channel.name).strip() + ", duration " + timeString)

		print(Lutils.TitleBox("Logging Into Discord"))
		
		print("Attempting to log in.")
		try:
			self.client.run(username, password)
		except Exception as e:
			print("ERROR logging into Discord! (" + str(e) + ")")
			input("Press enter to exit.\n")
			quit()