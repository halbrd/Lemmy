# Lemmy's stuff
import LemmyUtils as Lutils
import LemmyRadio as Lradio
import RandomLenny

# Other stuff
import random
import discord
import asyncio
import os
from os import listdir
from os.path import isfile, join
import json
import sqlite3
import datetime
from PIL import Image
import re
import urllib.request as req
from fuzzywuzzy import fuzz
import copy

async def help(self, msg, dmsg):
	reply = "Lemmy reference page: http://lynq.me/lemmy"
	reply += "\n"
	reply += "\nCommand terminology: `!command parameter -flag flagParameter`"
	reply += "\n\n```"

	commands = []
	for commandText, commandInfo in self.config.command.items():
		notes = []
		if not commandInfo["enabled"]: notes.append("disabled")
		if commandInfo["moderator"]: notes.append("moderator+")

		command = self.config.symbol[msg.server.id] + commandText + "    " + ("[" if len(notes) > 0 else "") + ", ".join(notes) + ("]" if len(notes) > 0 else "")
		command += "\n    " + commandInfo["description"]

		commands.append(command)
	reply += "\n".join(commands)
	reply += "\n```"

	await self.client.send_message(msg.channel, reply)

async def emotes(self, msg, dmsg):
	await self.client.send_message(msg.channel, "http://lynq.me/lemmy/#emotes")

async def stickers(self, msg, dmsg):
	await self.client.send_message(msg.channel, "http://lynq.me/lemmy/#stickers")

async def lenny(self, msg, dmsg):
	if len(dmsg.flags) == 0:
		await self.client.send_message(msg.channel, self.res.lennies[random.randint(0, len(self.res.lennies)-1)])
	else:
		for fullFlag in dmsg.flags:
			flag = fullFlag[0]
			if flag == "-og":
				await self.client.send_message(msg.channel, self.res.lenny)
			elif flag == "-r":
				await self.client.send_message(msg.channel, RandomLenny.randomLenny())

async def logout(self, msg, dmsg):
	print("User with id " + str(msg.author.id) + " attempting to initiate logout.")
	if not Lutils.IsAdmin(msg.author):
		await self.client.send_message(msg.channel, self.constants.error.symbol + " User is not admin.")
	else:
		await self.client.send_message(msg.channel, "Shutting down.")
		await self.client.logout()

async def refresh(self, msg, dmsg):
	refreshedEmotes = [ os.path.splitext(f)[0] for f in listdir("pics/emotes") if isfile(join("pics/emotes",f)) ]
	refreshedStickers = [ os.path.splitext(f)[0] for f in listdir("pics/stickers") if isfile(join("pics/stickers",f)) ]

	newEmotes = [item for item in refreshedEmotes if item not in self.res.emotes]
	newStickers = [item for item in refreshedStickers if item not in self.res.stickers]

	self.res.emotes = refreshedEmotes
	self.res.stickers = refreshedStickers

	if len(newEmotes) > 0:
		await self.client.send_message(msg.channel, "__**New emotes:**__")

		for emote in newEmotes:
			await self.client.send_message(msg.channel, emote)
			await self.client.send_file(msg.channel, "pics/emotes/" + emote + ".png")

	if len(newStickers) > 0:
		await self.client.send_message(msg.channel, "__**New stickers:**__")

		for sticker in newStickers:
			await self.client.send_message(msg.channel, sticker)
			await self.client.send_file(msg.channel, "pics/stickers/" + sticker + ".png")

	await self.client.delete_message(msg)

async def correct(self, msg, dmsg):
	await self.client.send_message(msg.channel, "https://youtu.be/OoZN3CAVczs")

async def eightball(self, msg, dmsg):
	responses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes, definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
	await self.client.send_message(msg.channel, msg.author.mention + " :8ball: " + random.choice(responses))

async def userinfo(self, msg, dmsg):
	if len(dmsg.params) > 0:
		username = dmsg.params[0]
		user = Lutils.FindUserByName(msg.channel.server.members, username)
		if not user:
			await self.client.send_message(msg.channel, self.constants.error.symbol + " User not found.")
		else:
			message = "**Username:** " + user.name + "\n**ID:** " + user.id + "\n**Join date:** " + str(user.joined_at)

			balance = Lutils.GetLemmyCoinBalance(self.res, user)
			if balance is not None:
				message += "\n**LemmyCoin Balance:** L$" + str(balance)

			message += "\n**Avatar URL:** " + user.avatar_url

			if user.voice_channel is not None:
				message += "\nCurrently talking in " + user.voice_channel.mention + "."

			# if user.game_id is not None:
			# 	message += "\nCurrent playing " + str(user.game_id) + "."

			await self.client.send_message(msg.channel, message)
			await self.client.send_message("Note: This command is deprecated; use Discord's Developer Mode to get IDs.")

async def channelinfo(self, msg, dmsg):
	if len(dmsg.params) > 0:
		channelName = dmsg.params[0]
		channel = discord.utils.find(lambda m: m.name == channelName, [x for x in msg.channel.server.channels if x.type == discord.ChannelType.text])
		if not channel:
			await self.client.send_message(msg.channel, self.constants.error.symbol + " Channel not found.")
		else:
			await self.client.send_message(msg.channel, "**Channel name: **" + channel.mention + "\n**ID: **" + channel.id)
		await self.client.send_message("Note: This command is deprecated; use Discord's Developer Mode to get IDs.")

async def james(self, msg, dmsg):
	if len(dmsg.params) > 0:
		sentTags = []
		for tag in dmsg.params:
			if tag in self.tags.db and tag not in sentTags:
				sentTags.append(tag)
				if msg.author.id not in self.tags.db[tag]:
					await self.client.send_message(msg.channel, self.constants.error.symbol + " User must be subscribed to the tag to issue pings.")
				else:
					await self.client.send_message(msg.channel, Lutils.GetPingText(self, msg, tag))

	for fullFlag in dmsg.flags:
		flag = fullFlag[0]
		flagParams = fullFlag[1:] if len(fullFlag) > 1 else []
		update = False

		if flag == "-tags":
			response = "```"
			for key in self.tags.db:
				response += "\n" + key + " (" + self.tags.converter[key] + ")\n"
				userNames = []
				for userId in self.tags.db[key]:
					user = Lutils.FindUserById(msg.channel.server.members, userId)
					if user:
						userNames.append(user.name)
				response += "> " + ", ".join(userNames)
				response += "\n"
			response += "```"
			await self.client.send_message(msg.channel, response)

		elif flag == "-join":
			if len(flagParams) == 0:
				await self.client.send_message(msg.channel, self.constants.error.symbol + " " + msg.author.mention + " was not added to any tag: No tag was specified.")
			else:
				gameTag = flagParams[0]
				if not gameTag in self.tags.db:
					await self.client.send_message(msg.channel, self.constants.error.symbol + " " + msg.author.mention + " was not added to '" + gameTag + "': No such tag exists.")
				else:
					if msg.author.id in self.tags.db[gameTag]:
						await self.client.send_message(msg.channel, self.constants.error.symbol + " " + msg.author.mention + " was not added to '" + gameTag + "': User is already in '" + gameTag + "'.")
					else:
						update = True
						self.tags.db[gameTag].append(msg.author.id)
						await self.client.send_message(msg.channel, msg.author.mention + " was successfully added to '" + gameTag + "'.")
					
		elif flag == "-leave":
			if len(flagParams) == 0:
				await self.client.send_message(msg.channel, self.constants.error.symbol + " " + msg.author.mention + " was not removed from any tag: No tag was specified.")
			else:
				gameTag = flagParams[0]
				if not gameTag in self.tags.db:
					await self.client.send_message(msg.channel, self.constants.error.symbol + " " + msg.author.mention + " was not removed from '" + gameTag + "': No such tag exists.")
				else:
					if not msg.author.id in self.tags.db[gameTag]:
						await self.client.send_message(msg.channel, self.constants.error.symbol + " " + msg.author.mention + " was not removed from '" + gameTag + "': User is not in '" + gameTag + "'.")
					else:
						update = True
						self.tags.db[gameTag] = [x for x in self.tags.db[gameTag] if x != msg.author.id]
						await self.client.send_message(msg.channel, msg.author.mention + " was successfully removed from '" + gameTag + "'.")

		elif flag == "-create":
			if not Lutils.IsModOrAbove(msg.author):
				await self.client.send_message(msg.channel, self.constants.error.symbol + " No new tag created: " + self.constants.error.notMod)
			else:
				if len(flagParams) == 0:
					await self.client.send_message(msg.channel, self.constants.error.symbol + " No new tag created: No tag name was specified.")
				else:
					if len(flagParams) == 1:
						await self.client.send_message(msg.channel, self.constants.error.symbol + " New tag '" + flagParams[0] + "' not created: No display name was given.")
					else:
						gameTag = flagParams[0]
						displayName = " ".join(flagParams[1:])

						if gameTag in self.tags.db:
							await self.client.send_message(msg.channel, self.constants.error.symbol + " New tag '" + gameTag + "' not created: Tag already exists.")
						else:
							update = True
							self.tags.db[gameTag] = []
							self.tags.converter[gameTag] = displayName
							await self.client.send_message(msg.channel, "New tag '" + gameTag + "' successfully created with display name '" + displayName + "'.")

		elif flag == "-delete":
			if not Lutils.IsModOrAbove(msg.author):
				await self.client.send_message(msg.channel, self.constants.error.symbol + " No tag deleted: " + self.constants.error.notMod)
			else:
				if len(flagParams) == 0:
					await self.client.send_message(msg.channel, self.constants.error.symbol + " No tag deleted: No tag name was specified.")
				else:
					gameTag = flagParams[0]
					if not gameTag in self.tags.db:
						await self.client.send_message(msg.channel, self.constants.error.symbol + " Tag '" + gameTag + "' not deleted: Tag does not exist.")
					else:
						update = True
						self.tags.db.pop(gameTag, None)
						self.tags.converter.pop(gameTag, None)
						await self.client.send_message(msg.channel, "Tag '" + gameTag + "' successfully deleted.")

		if update:
			try:
				with open("db/tagDb.json", "w") as f:
					json.dump(self.tags.db, f, indent=4)
			except Exception as e:
				print("ERROR updating tagDb! (" + str(e) + ")")
			else:
				print("tagDb updated with " + str(len(self.tags.db)) + " games.")

			try:
				with open("db/tagConverter.json", "w") as f:
					json.dump(self.tags.converter, f, indent=4)
			except Exception as e:
				print("ERROR updating tagConverter! (" + str(e) + ")")
			else:
				print("tagConverter updated with " + str(len(self.tags.converter)) + " games.")

			await self.client.send_message(msg.channel, "Note: !james is deprecated, and has been replaced with native Discord roles and the !role command. Use @tag to ping a tag.")

async def role(self, msg, dmsg):
	# List roles
	# Add role
	# Delete role
	# Make james perform these actions

	# Load role metadata
	with open("db/config/roles.json", "r") as f:
		roleData = json.load(f)

	for fullFlag in dmsg.flags:
		flag = fullFlag[0]
		param1 = fullFlag[1] if len(fullFlag) > 1 else None
		param2 = fullFlag[2] if len(fullFlag) > 2 else None
		
		if flag == "-allow" or flag == "-deny":
			allow = flag == "-allow"
			if not Lutils.IsModOrAbove(msg.author):
				await self.client.send_message(msg.channel, self.constants.error.symbol + " No role changed: " + self.constants.error.notMod)
			else:
				if param1 is None:
					await self.client.send_message(msg.channel, self.constants.error.symbol + " No role changed: No role name was specified.")
				else:
					role = discord.utils.get(msg.server.roles, mention=param1)
					if role is None:
						role = discord.utils.get(msg.server.roles, name=param1)

					if role is None:
						await self.client.send_message(msg.channel, self.constants.error.symbol + " No role changed: Role '" + param1 + "' does not exist.")
					else:
						roleData[role.id] = allow
						await self.client.send_message(msg.channel, "Role '" + role.name + "' set to " + ("allow" if allow else "deny") + " joining.")

		elif flag == "-join" or flag == "-leave":
			join = flag == "-join"
			if param1 is None:
				await self.client.send_message(msg.channel, self.constants.error.symbol + " Role not " + ("joined" if join else "left") + ": No role name provided.")
			else:
				role = discord.utils.get(msg.server.roles, mention=param1)
				if role is None:
					role = discord.utils.get(msg.server.roles, name=param1)

				if role is None:
					await self.client.send_message(msg.channel, self.constants.error.symbol + " Role not " + ("joined" if join else "left") + ": Role '" + param1 + "' does not exist.")
				else:
					if not (role.id in roleData and roleData[role.id]):
						await self.client.send_message(msg.channel, self.constants.error.symbol + " Role not " + ("joined" if join else "left") + ": Role '" + role.name + "' is not set to accept automated " + ("joining" if join else "leaving") + ".")
					else:
						if join:
							await self.client.add_roles(msg.author, role)
						else:
							await self.client.remove_roles(msg.author, role)
						await self.client.send_message(msg.channel, "User " + msg.author.mention + " " + ("added to" if join else "removed from") + " " + role.name + ".")

		elif flag == "-add" or flag == "-remove":
			add = flag == "-add"
			if not Lutils.IsModOrAbove(msg.author):
				await self.client.send_message(msg.channel, self.constants.error.symbol + " No role changed: " + self.constants.error.notMod)
			else:
				if param1 is None:
					await self.client.send_message(msg.channel, self.constants.error.symbol + " User not " + ("added to" if add else "removed from") + " role: No user name provided.")
				else:
					if param2 is None:
						await self.client.send_message(msg.channel, self.constants.error.symbol + " User not " + ("added to" if add else "removed from") + " role: No role provided.")
					else:
						user = discord.utils.get(msg.server.members, mention=param1)
						if user is None:
							user = discord.utils.get(msg.server.members, name=param1)

						role = discord.utils.get(msg.server.roles, mention=param2)
						if role is None:
							role = discord.utils.get(msg.server.roles, name=param2)

						if user is None:
							await self.client.send_message(msg.channel, self.constants.error.symbol + " User not " + ("added to" if add else "removed from") + " role: User '" + param1 + "' does not exist.")
						elif role is None:
							await self.client.send_message(msg.channel, self.constants.error.symbol + " User not " + ("added to" if add else "removed from") + " role: Role '" + param2 + "' does not exist.")
						else:
							if not (role.id in roleData and roleData[role.id]):
								await self.client.send_message(msg.channel, self.constants.error.symbol + " User " + user.name + " not " + ("added to" if add else "removed from") + " role " + role.name + ": Role '" + role.name + "' is not set to accept automated " + ("joining" if add else "leaving") + ".")
							else:
								if add:
									await self.client.add_roles(user, role)
								else:
									await self.client.remove_roles(user, role)
								await self.client.send_message(msg.channel, "User " + user.mention + " " + ("added to" if add else "removed from") + " " + role.name + ".")

		tempDict = copy.deepcopy(roleData)
		for key in roleData:
			role = discord.utils.get(msg.channel.server.roles, id=key)
			if role is None:
				del tempDict[key]
		roleData = tempDict

	try:
		with open("db/config/roles.json", "w") as f:
			json.dump(roleData, f, indent=4)
	except Exception as e:
		print("ERROR updating roleData! (" + str(e) + ")")
	else:
		print("roleData updated.")


async def happening(self, msg, dmsg):
	await self.client.send_message(msg.channel, "https://i.imgur.com/bYGOUHP.gif")

async def ruseman(self, msg, dmsg):
	await self.client.send_file(msg.channel, "pics/ruseman/" + random.choice(os.listdir("pics/ruseman/")))

async def lemmycoin(self, msg, dmsg):
	for fullFlag in dmsg.flags:
		flag = fullFlag[0]
		param1 = fullFlag[1] if len(fullFlag) > 1 else None
		param2 = fullFlag[2] if len(fullFlag) > 2 else None

		if flag == "-balance" or flag == "-b":
			user = None

			if param1 is None:
				user = msg.author
			else:
				targetUser = Lutils.FindUserByName(msg.channel.server.members, param1)
				if targetUser is None:
					await self.client.send_message(msg.channel, self.constants.error.symbol + " User '" + param1 + "' was not found on this Discord server.")
				else:
					user = targetUser

			if user is not None:
				balance = Lutils.GetLemmyCoinBalance(self.res, user)

				if balance is None:
					await self.client.send_message(msg.channel, self.constants.error.symbol + " " + user.name + " does not have a LemmyCoin balance because they have not been registered in the database.")
				else:
					await self.client.send_message(msg.channel, user.name + " has a LemmyCoin balance of L$" + str(balance) + ".")

		elif flag == "-pay" or flag == "-p":
			if param1 is not None:
				target = Lutils.FindUserByName(msg.channel.server.members, param1)
				if target is None:
					await self.client.send_message(msg.channel, self.constants.error.symbol + " LemmyCoins not sent: User '" + param1 + "' was not found on this server.")
				elif param2 is None:
					await self.client.send_message(msg.channel, self.constants.error.symbol + " No LemmyCoins paid to " + target.name + ": No amount was specified.")
				else:
					try:
						amount = float(param2)
					except ValueError:
						await self.client.send_message(msg.channel, self.constants.error.symbol + " No LemmyCoins paid to " + target.name + ": Amount was incorrectly formatted.")
					else:
						if amount <= 0:
							await self.client.send_message(msg.channel, self.constants.error.symbol + " No LemmyCoins paid to " + target.name + ": Amount must be greater than zero.")
						else:
							cursor = self.res.sqlConnection.cursor()
							cursor.execute("SELECT COUNT(*) FROM tblUser WHERE UserId = ?", (target.id,))
							result = cursor.fetchone()[0]

							if result == 0:
								await self.client.send_message(msg.channel, self.constants.error.symbol + " No LemmyCoins paid to " + target.name + ": " + target.name + " has not been registered in the database.")
							else:
								cursor.execute("SELECT LemmyCoinBalance FROM tblUser WHERE UserId = ?", (msg.author.id,))
								senderBalance = cursor.fetchone()[0]

								if senderBalance < amount:
									await self.client.send_message(msg.channel, self.constants.error.symbol + " No LemmyCoins paid to " + target.name + ": " + msg.author.mention + " does not have enough LemmyCoins in their account to make the payment.")
								else:
									cursor.execute("UPDATE tblUser SET LemmyCoinBalance = LemmyCoinBalance - ? WHERE UserId = ?", (amount, msg.author.id))
									cursor.execute("UPDATE tblUser SET LemmyCoinBalance = LemmyCoinBalance + ? WHERE UserId = ?", (amount, target.id))
									cursor.execute("INSERT INTO tblLemmyCoinPayment (DateTime, SenderId, ReceiverId, Amount) VALUES (?, ?, ?, ?)", (datetime.datetime.now(), msg.author.id, target.id, amount))
									self.res.sqlConnection.commit()
									await self.client.send_message(msg.channel, "**L$" + str(amount) + "** successfully sent to " + target.mention + " by " + msg.author.mention + ".")

async def channelids(self, msg, dmsg):
	ret = ""
	for channel in msg.channel.server.channels:
		ret += channel.name + " : " + channel.id + "\n"
	await self.client.send_message(msg.channel, ret)
	await self.client.send_message("Note: This command is deprecated; use Discord's Developer Mode to get IDs.")

async def serverinfo(self, msg, dmsg):
	#await self.client.send_message(msg.channel, msg.channel.server.name + ": " + msg.channel.server.id)
	server = msg.server
	response = "**Name:** " + server.name
	response += "\n**Region:** " + str(server.region)
	response += "\n**Owner:** " + server.owner.name
	response += "\n**Population:** " + str(len(server.members)) + " (" + str(len([member for member in server.members if member.status != discord.Status.offline])) + " currently online)"
	response += "\n**Roles:** "
	for role in server.roles:
		response += "\n  " + ("everyone" if role.name == "@everyone" else role.name)
	response += "\n**Default channel:** " + server.default_channel.name
	response += "\n**AFK channel:** " + (server.afk_channel.name if server.afk_channel is not None else "None")
	response += "\n**AFK timeout length:** " + str(server.afk_timeout) + " minutes"
	response += "\n**Icon URL:** " + server.icon_url


	await self.client.send_message(msg.channel, response)

async def choose(self, msg, dmsg):
	params = ["OR" if x.lower() == "or" else x for x in dmsg.params]
	options = " ".join(params).split(" OR ")
	options = [x for x in options if x != ""]
	if len(options) > 0:
		# await self.client.send_message(msg.channel, msg.author.mention + "\n```\n" + random.choice(options) + "\n```")
		await self.client.send_message(msg.channel, msg.author.mention + "   `" + random.choice(options) + "`")

async def tts(self, msg, dmsg):
	await self.client.send_message(msg.channel, msg.content[5:], tts=True)
	await self.client.delete_message(msg)

async def playgame(self, msg, dmsg):
	await self.client.change_status(game=(discord.Game(name=dmsg.params[0]) if len(dmsg.params) > 0 else None))

async def tilt(self, msg, dmsg):
	if len(dmsg.params) > 0:
		#urllib.request.urlretrieve(msg.author.avatar_url, "pics/temp/avatar.jpg")
		#Lutils.RotateImage("pics/temp/avatar.jpg")
		imgName = dmsg.params[0]
		if not imgName in self.res.emotes and not imgName in self.res.stickers:
			await self.client.send_message(msg.channel, self.constants.error.symbol + " Emote or sticker '" + imgName + "' not found.")
		else:
			send = True
			angle = 45
			if len(dmsg.params) > 1:
				try:
					angle = int(dmsg.params[1])
				except ValueError:
					await self.client.send_message(msg.channel, self.constants.error.symbol + " Incorrectly formatted angle value.")
					send = false

			if send:
				if imgName in self.res.emotes:
					Lutils.RotateImage("pics/emotes/" + dmsg.params[0] + ".png", angle * -1)
				elif imgName in self.res.stickers:
					Lutils.RotateImage("pics/stickers/" + dmsg.params[0] + ".png", angle * -1)
				await Lutils.SendTemp(self.client, msg)

async def radio(self, msg, dmsg):
	#await self.client.send_message(msg.channel, self.constants.error.symbol + " This command has been disabled due to the overwhelming probability that everything will explode upon invocation.")

	for fullFlag in dmsg.flags:
		flag = fullFlag[0]

		if flag == "-init":
			self.radio.radioChannel = Lutils.FindChannelById(msg.server.channels, self.config.radioVoiceChannel[msg.server.id])
			self.radio.infoChannel = Lutils.FindChannelById(msg.server.channels, self.config.radioInfoChannel[msg.server.id])
			self.radio.voiceConnection = await self.client.join_voice_channel(self.radio.radioChannel)

		elif flag == "-exit":
			await self.radio.voiceConnection.disconnect()
			self.radio.radioChannel = None
			self.radio.infoChannel = None

		elif flag == "-pause":
			await self.radio.Pause()

		elif flag == "-resume":
			await self.radio.Resume()

		elif flag == "-queue":
			if len(fullFlag) == 1:
				await self.client.send_message(msg.channel, self.constants.error.symbol + " No source was given.")
			else:
				source = fullFlag[1]
				song = Lradio.Song("youtube", source, "Placeholder Youtube Title")
				await self.radio.QueueSong(song)

		elif flag == "-next":
			self.radio.NextSong()

		elif flag == "-prev":
			self.radio.PrevSong()

		elif flag == "-viewqueue":
			await self.client.send_message(msg.channel, str([x.source for x in self.radio.queue]))

		elif flag == "-shuffletag":
			if len(fullFlag) < 2:
				await self.client.send_message(msg.channel, self.constants.error.symbol + " No tag was given.")
			else:
				tag = fullFlag[1]
				tagConverter = {
					"cafe del mar": "Cafe Del Mar",
					"payday": "PAYDAY 2 Official Soundtrack"
				}

				if tag.lower() not in tagConverter:
					await self.client.send_message(msg.channel, self.constants.error.symbol + " Tag not recognized (available tags: " + ", ".join([x for x in tagConverter]) + ")")
				else:
					convertedTag = tagConverter[tag]
					await self.radio.ShuffleTag(self.client, convertedTag)

		elif flag == "-playyt":
			if len(fullFlag) < 2:
				await self.client.send_message(msg.channel, self.constants.error.symbol + " No URL was given")
			else:
				url = fullFlag[1]
				try:
					await self.radio.PlayYoutubeVideo(self.client, url)
				except Exception as e:
					await self.client.send_message(msg.channel, self.constants.error.symbol + " " + str(e))

		elif flag == "-interlude":
			await self.radio.LoopSong("N:\\Misc\\Interlude.m4a")

async def skypeemotes(self, msg, dmsg):
	await self.client.send_message(msg.channel, "   ".join(self.res.skype.emotes))
	
async def shrug(self, msg, dmsg):
	await self.client.send_message(msg.channel, "¯\\_(ツ)_/¯")

async def thisisfine(self, msg, dmsg):
	#await self.client.send_file(msg.channel, "pics/originals/ThisIsFine.png")
	await self.client.send_message(msg.channel, "http://i.imgur.com/YfAZJky.png")

async def lol(self, msg, dmsg):
	for fullFlag in dmsg.flags:
		flag = fullFlag[0]

		if flag == "-item":
			searchTerm = " ".join(fullFlag[1:])
			if searchTerm == "":
				await self.client.send_message(msg.channel, self.constants.error.symbol + " No search term given.")
			else:
				itemResp = req.urlopen("https://global.api.pvp.net/api/lol/static-data/oce/v1.2/item?api_key=fc9a7992-b45f-46a9-ad2f-9f35608aee36")

				if not itemResp.getcode() != "200":
					await self.client.send_message(msg.channel, "HTTP code " + itemResp.getcode())
				else:
					itemData = json.loads(itemResp.read().decode("utf-8"))["data"]

					nameMap = {}
					searchMap = []
					for itemId in itemData:
						nameMap[itemData[itemId]["name"]] = itemId
						searchMap.append([fuzz.ratio(searchTerm, itemData[itemId]["name"]), itemData[itemId]["name"]])
					searchMap.sort(reverse=True)
					#await self.client.send_message(msg.channel, "datalen=" + str(len(itemData)) + "\nsearchmaplen=" + str(len(searchMap)))

					#d = str(searchMap)
					#d = [d[i:i+2000] for i in range(0, len(d), 2000)]
					#for chunk in d:
					#	await self.client.send_message(msg.channel, chunk)
					
					matchName = searchMap[0][1]
					matchId = nameMap[matchName]
					matchDesc = itemData[matchId]["description"]
					matchDesc = re.sub("<br>", "\n", matchDesc)
					matchDesc = re.sub("<\/?[a-zA-Z]*>", "", matchDesc)
					await self.client.send_message(msg.channel, "**" + matchName + "**\n" + matchDesc)




# async def radio(self, msg, dmsg):
# 	# radioChannel = discord.utils.find(lambda m: m.id == "133010408377286656", msg.server.channels)
# 	# if not radioChannel:
# 	# 	await client.send_message(msg.channel, "Radio channel not found.")
# 	# else:
# 	# 	voice = await client.join_voice_channel(radioChannel)
# 	# 	player = voice.create_ffmpeg_player("audio/songs/sirens_in_the_distance.mp3")
# 	# 	player.start()

# 	flag = Lutils.GetNthFlagWithAllParams(1, params)[0]
# 	flagParams = Lutils.GetNthFlagWithAllParams(1, params)[1:]

# 	if flag == "-quick":
# 		musicDir = "N:\Cafe Del Mar"
# 		await client.send_message(msg.channel, "Queueing directory " + musicDir)
# 		res.radio.QueueDirectory(musicDir)
# 		await client.send_message(msg.channel, "Directory queued. New queue size: " + str(res.radio.queue.qsize()))
		
# 		res.radio.ShuffleQueue()
# 		await client.send_message(msg.channel, "Queue shuffled.")

# 		radioChannel = res.radio.GetRadioChannel()
# 		voice = await client.join_voice_channel(radioChannel)
# 		res.radio.SetVoiceConnection(voice)
# 		while not res.radio.queue.empty():
# 			res.radio.StartNextSong()
# 			#await client.send_message(res.radio.GetInfoChannel(), res.radio.GetCurrentSong())

# 	elif flag == "-queuedir":
# 		await client.send_message(msg.channel, "Queueing directory " + flagParams[0])
# 		res.radio.QueueDirectory(flagParams[0])
# 		await client.send_message(msg.channel, "Directory queued. New queue size: " + str(res.radio.queue.qsize()))

# 	elif flag == "-shuffle":
# 		res.radio.ShuffleQueue()
# 		await client.send_message(msg.channel, "Queue shuffled.")

# 	elif flag == "-play":
# 		radioChannel = res.radio.GetRadioChannel()
# 		voice = await client.join_voice_channel(radioChannel)
# 		res.radio.SetVoiceConnection(voice)
# 		while not res.radio.queue.empty():
# 			res.radio.StartNextSong()
# 			#await client.send_message(res.radio.GetInfoChannel(), res.radio.GetCurrentSong())

# 	elif flag == "-stop":
# 		res.radio.StopPlayer()

# 	elif flag == "-pause":
# 		res.radio.PausePlayer()

# 	elif flag == "-resume":
# 		res.radio.ResumePlayer()

# 	elif flag == "-clear":
# 		res.radio.ClearQueue()
# 		await client.send_message(msg.channel, "Queue cleared. [DEBUG] len(queue)=" + str(res.radio.queue.qsize()))

# 	# elif flag == "-nowplaying":
# 	# 	await client.send_message(msg.channel, res.radio.GetCurrentSong())

# 	elif flag == "-viewqueue":
# 		await client.send_message(msg.channel, res.radio.ViewQueue())

#####################
# Archived commands #
#####################

# def register(client, res, msg, params):
# 	if Lutils.IsAdmin(msg.author):
# 		if len(params) > 0:
# 			userId = params[0]
			
# 			cursor = res.sqlConnection.cursor()
# 			cursor.execute("SELECT COUNT(*) FROM tblUser WHERE UserId = ?", (userId,))
# 			if cursor.fetchone()[0] > 0:
# 				await client.send_message(msg.channel, "User with id " + userId + " not registered to database: User already exists in database.")
# 			else:
# 				user = Lutils.FindUserById(msg.channel.server.members, userId)
# 				if not user:
# 					await client.send_message(msg.channel, "User with id " + userId + " not registered to database: ID does not reference a Discord user on this server.")
# 				else:
# 					cursor.execute("INSERT INTO tblUser (UserId, LemmyCoinBalance) VALUES (?, 10)", (userId,))
# 					res.sqlConnection.commit()
# 					await client.send_message(msg.channel, "User with id " + userId + " (" + user.mention + ") successfully registered to database.")

# async def combine(self, msg, dmsg):
# 	# This command is deprecated, since it's a native feature of the bot
# 	allEmotes = True
# 	for param in params:
# 		if param not in res.emotes and param not in res.stickers:
# 			allEmotes = False

# 	if allEmotes:
# 		images = []
# 		for param in params:
# 			try:
# 				images.append(Image.open("pics/emotes/" + param + ".png"))
# 			except IOError:
# 				images.append(Image.open("pics/stickers/" + param + ".png"))

# 	Lutils.CombineImages(images)

# 	await client.send_file(msg.channel, "pics/result.png")