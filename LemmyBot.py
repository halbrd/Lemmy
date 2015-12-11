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
import datetime
import codecs

class LemmyBot:
	def __init__(self, username, password):
		self.res = Lres.LemmyResources()
		self.res.Load()

		# Map of function names to their equivalent function pointers
		self.funcMap = {
			"help": Lcmds.help,
			"emotes": Lcmds.emotes,
			"stickers": Lcmds.stickers,
			"lenny": Lcmds.lenny,
			"refresh": Lcmds.refresh,
			"F5": Lcmds.refresh,
			"correct": Lcmds.correct,
			"8ball": Lcmds.eightball,
			"userinfo": Lcmds.userinfo,
			"channelinfo": Lcmds.channelinfo,
			"james": Lcmds.james,
			"happening": Lcmds.happening,
			"ruseman": Lcmds.ruseman,
			"register": Lcmds.register,
			#"lemmycoin": Lcmds.lemmycoin,
			"logout": Lcmds.logout
		}

		self.floodProtectors = {
			"emote": FloodProtector(5),
			"sticker": FloodProtector(5)
		}

		self.callLogger = None

		self.client = discord.Client()
		print("\n========================\n= Logging Into Discord =\n========================\n")
		
		print("Attempting to log in.")
		try:
			self.client.login(username, password)
		except:
			print("ERROR logging into Discord!")
			input("Press any key to exit.\n")
			quit()

		@self.client.event
		def on_ready():
			print("Successfully logged in.")
			print("USERNAME: " + username)
			print("PASSWORD: " + "".join(["*" for x in password]))
			print("\n==========================\n= Listening For Messages =\n==========================\n")

			channelList = []
			for server in self.client.servers:
				for channel in server.channels:
					if channel.type == "voice":
						channelList.append(channel)
			self.callLogger = CallLogger(channelList)

		@self.client.event
		def on_message(msg):
			if msg.content:
				if msg.channel.is_private:
					print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " + msg.author.name + " => (private channel): " + msg.content)
				else:
					print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " + msg.author.name + " => " + msg.channel.name + ": " + msg.content)

				if msg.content[0] == "!":
					dmsg = Lutils.GetDecomposedMessage(msg.content)

					if dmsg.command in self.funcMap:
						self.funcMap[dmsg.command](self.client, self.res, msg, dmsg.params)

				elif msg.content in self.res.emotes and msg.author != self.client.user:
					if self.floodProtectors["emote"].Ready(msg.author.id):
						Lutils.SendEmote(self.client, msg)
						self.floodProtectors["emote"].Sent(msg.author.id)
					else:
						self.client.delete_message(msg)

				elif msg.content in self.res.stickers and msg.author != self.client.user:
					if self.floodProtectors["sticker"].Ready(msg.author.id):
						Lutils.SendSticker(self.client, msg)
						self.floodProtectors["sticker"].Sent(msg.author.id)
					else:
						self.client.delete_message(msg)

			else:
				if msg.channel.is_private:
					print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " + msg.author.name + " => (private channel): (Non-text message or file)")
				else:
					print("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] " + msg.author.name + " => " + msg.channel.name + ": (Non-text message or file)")

		@self.client.event
		def on_voice_state_update(member):
			channelList = []
			for server in self.client.servers:
				for channel in server.channels:
					if channel.type == "voice":
						channelList.append(channel)
			responses = self.callLogger.UpdateStatuses(channelList)

			for response in responses:
				channel = response[0]
				timeString = response[1]
				self.client.send_message(discord.utils.find(lambda m: m.name == "lemmybot", channel.server.channels), "Call ended in " + Lutils.StripUnicode(channel.name).strip() + ", duration " + timeString)

	def Start(self):
		self.client.run()