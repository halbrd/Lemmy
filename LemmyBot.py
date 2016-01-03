import sys
sys.path.append('modules')

# Lemmy's stuff
import LemmyUtils as Lutils
import LemmyCommands as Lcmds
import LemmyResources as Lres
from FloodProtector import FloodProtector
from CallLogger import CallLogger

# Other stuff
import discord
import asyncio
import datetime
import codecs

class LemmyBot:
	def __init__(self, username, password):
		self.res = Lres.LemmyResources()
		self.res.Load()

		self.commandSymbol = "?>"

		# Map of function names to their equivalent function pointers
		self.funcMap = {
			"help": Lcmds.help,
			"emotes": Lcmds.emotes,
			"stickers": Lcmds.stickers,
			"lenny": Lcmds.lenny,
			"refresh": Lcmds.refresh,
			"f5": Lcmds.refresh,
			"correct": Lcmds.correct,
			"8ball": Lcmds.eightball,
			"userinfo": Lcmds.userinfo,
			"channelinfo": Lcmds.channelinfo,
			"james": Lcmds.james,
			"happening": Lcmds.happening,
			"ruseman": Lcmds.ruseman,
			"lemmycoin": Lcmds.lemmycoin,
			"lc": Lcmds.lemmycoin,
			"l$": Lcmds.lemmycoin,
			"channelids": Lcmds.channelids,
			"serverid": Lcmds.serverid,
			"logout": Lcmds.logout
			#"restart": Lcmds.restart
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


			print(Lutils.TitleBox("Checking Channel Mapping"))
			warnings = False
			for server in self.client.servers:

				# Server hasn't been mapped at all
				if server.id not in self.res.voiceToTextChannelMaps and server.id not in self.res.textToVoiceChannelMaps:
					print("Warning! Server " + server.name + " does not have its voice or text channels mapped.")
					warnings = True

				# Server has had text channels mapped, but not voice channels
				elif server.id not in self.res.voiceToTextChannelMaps:
					print("Warning! Server " + server.name + " does not have its voice channels mapped.")
					warnings = True
					for channel in server.channels:
						if channel.type == discord.ChannelType.text and channel.id not in self.res.textToVoiceChannelMaps[server.id]:
							print("  Warning! Server " + server.name + "'s text channel " + channel.name + " has not been mapped to a voice channel (or None).")

				# Server has had voice channels mapped, but not text channels
				elif server.id not in self.res.textToVoiceChannelMaps:
					print("Warning! Server " + server.name + " does not have its text channels mapped.")
					warnings = True
					for channel in server.channels:
						if channel.type == discord.ChannelType.voice and channel.id not in self.res.voiceToTextChannelMaps[server.id]:
							print("  Warning! Server " + server.name + "'s voice channel " + Lutils.StripUnicode(channel.name).strip() + " has not been mapped to a text channel (or None).")

				# Server has had voice and text channels mapped
				else:
					print("Server " + server.name + " has its voice and text channels mapped.")
					for channel in server.channels:
						if channel.type == discord.ChannelType.text and channel.id not in self.res.textToVoiceChannelMaps[server.id]:
							print("Warning! Server " + server.name + "'s text channel " + channel.name + " has not been mapped to a voice channel (or None).")
							warnings = True
					for channel in server.channels:
						if channel.type == discord.ChannelType.voice and channel.id not in self.res.voiceToTextChannelMaps[server.id]:
							print("Warning! Server " + server.name + "'s voice channel " + Lutils.StripUnicode(channel.name).strip() + " has not been mapped to a text channel (or None).")
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
			if msg.content:
				if msg.channel.is_private:
					print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " + msg.author.name + " => (private channel): " + Lutils.RemoveUnicode(msg.content))
				else:
					print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " + msg.author.name + " => " + msg.channel.name + ": " + Lutils.RemoveUnicode(msg.content))

				if msg.content.startswith("!"):
					await self.client.send_message(msg.channel, '"!" has been replaced by "?>"" as the command operator (eg. ?>lenny).')

				if msg.content.startswith(self.commandSymbol):
					dmsg = Lutils.ParseMessage(msg.content[len(self.commandSymbol):])

					if dmsg.command.lower() in self.funcMap:
						await self.funcMap[dmsg.command.lower()](self.client, self.res, msg, dmsg.params)

				elif msg.content in self.res.emotes and msg.author != self.client.user:
					if self.floodProtectors["emote"].Ready(msg.author.id):
						await Lutils.SendEmote(self.client, msg)
						self.floodProtectors["emote"].Sent(msg.author.id)
					else:
						await self.client.delete_message(msg)

				elif msg.content in self.res.stickers and msg.author != self.client.user:
					if self.floodProtectors["sticker"].Ready(msg.author.id):
						await Lutils.SendSticker(self.client, msg)
						self.floodProtectors["sticker"].Sent(msg.author.id)
					else:
						await self.client.delete_message(msg)

			else:
				if msg.channel.is_private:
					print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " + msg.author.name + " => (private channel): (Non-text message or file)")
				else:
					print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " + msg.author.name + " => " + msg.channel.name + ": (Non-text message or file)")

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