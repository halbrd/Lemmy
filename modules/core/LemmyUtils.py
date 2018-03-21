import discord
import asyncio
import shlex
from PIL import Image
import random
import datetime
import re
from math import sin, cos, ceil
import os
import os.path
import json

class DecomposedMessage:
	def __init__(self, command, params, flags):
		self.command = command
		self.params = params
		self.flags = flags

def ParseMessage(messageText):
	decomposedArray = shlex.split(messageText)

	command = decomposedArray[0].lower() if len(decomposedArray) > 0 else None

	params = []
	i = 1
	while i < len(decomposedArray) and decomposedArray[i][0] != "-":
		params.append(decomposedArray[i])
		i += 1

	flags = []
	while i < len(decomposedArray):
		if decomposedArray[i][0] == "-" and not re.fullmatch("-\d+(.\d+)?", decomposedArray[i]):
			flags.append([decomposedArray[i].lower()])
		else:
			flags[-1].append(decomposedArray[i])
		i += 1

	return DecomposedMessage(command, params, flags)

async def SendEmote(client, msg):
	if os.path.isfile("pics/emotes/" + msg.content + ".gif"):
		embed = discord.Embed()
		embed.set_image(url="http://lynq.me/lemmy/emotes/" + msg.content + ".gif")
		await client.send_message(msg.channel, msg.author.name, embed=embed)
	else:
		await client.send_file(msg.channel, "pics/emotes/" + msg.content + ".png", content=msg.author.name)
	await client.delete_message(msg)

async def SendSticker(client, msg):
	if os.path.isfile("pics/stickers/" + msg.content + ".gif"):
		embed = discord.Embed()
		embed.set_image(url="http://lynq.me/lemmy/stickers/" + msg.content + ".gif")
		await client.send_message(msg.channel, msg.author.name, embed=embed)
	else:
		await client.send_file(msg.channel, "pics/stickers/" + msg.content + ".png", content=msg.author.name)
	await client.delete_message(msg)

async def SendTemp(client, msg):
	#await client.send_message(msg.channel, "**" + msg.author.name + "**")
	await client.send_file(msg.channel, "pics/temp/temp.png", content=msg.author.name)
	await client.delete_message(msg)
	os.remove("pics/temp/temp.png")

async def SendSkypeEmote(client, msg):
	#await client.send_message(msg.channel, "**" + msg.author.name + "**")
	await client.send_file(msg.channel, "pics/skype/emotes/" + msg.content[1:-1] + ".gif", content=msg.author.name)
	await client.delete_message(msg)

async def SendSkypeFlag(client, msg):
	#await client.send_message(msg.channel, "**" + msg.author.name + "**")
	await client.send_file(msg.channel, "pics/skype/flags/" + msg.content[6:-1] + ".png", content=msg.author.name)
	await client.delete_message(msg)

def StripUnicode(string):
	stripped = [c for c in string if 0 < ord(c) < 127]
	return "".join(stripped)

def IsAdmin(member):
	#return "administrator" in [role.name for role in member.roles]
	return member.id == "77041679726551040"

def IsModOrAbove(member):
	return "administrator" in [role.name for role in member.roles] or "moderator" in [role.name for role in member.roles] or "robots" in [role.name for role in member.roles]

def IsRole(role, member):
	return role in [role.name for role in member.roles]

def FindUserByName(members, username):
	return discord.utils.find(lambda m: m.name == username, members)

def FindUserById(members, userId):
	return discord.utils.find(lambda m: m.id == userId, members)

def FindChannelById(channels, channelId):
	return discord.utils.find(lambda m: m.id == channelId, channels)

def GetLemmyCoinBalance(res, user):
	cursor = res.sqlConnection.cursor()
	cursor.execute("SELECT LemmyCoinBalance FROM tblUser WHERE UserId = ?", (user.id,))
	record = cursor.fetchone()
	return (record[0] if record is not None else None)

def RemoveUnicode(string):
	return "".join([i if ord(i) < 128 else ' ' for i in string])

def TitleBox(string):
	return "\n" + "".join(["=" for _ in range(len(string) + 4)]) + "\n= " + string + " =\n" + "".join(["=" for _ in range(len(string) + 4)]) + "\n"

def CombineImages(images):
	width = 0
	for image in images:
		width += image.size[0]

	height = max([image.size[1] for image in images])

	result = Image.new("RGBA", (width, height))

	i = 0
	horizontalPointer = 0
	while i < len(images):
		result.paste(images[i], (horizontalPointer, 0))
		horizontalPointer += images[i].size[0]
		i += 1

	result.save("pics/temp/temp.png")

def LogEmoteUse(res, sender, emote):
	cursor = res.sqlConnection.cursor()
	newId = random.uniform(0.0, 1.0)
	cursor.execute("INSERT INTO tblEmoteUse (DateTime, UserId, Emote) VALUES (?, ?, ?)", (datetime.datetime.now(), sender.id, emote))
	res.sqlConnection.commit()

async def LogMessage(msg):
	metadata = Colorize("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]", "black") + " " + Colorize(msg.author.name, "cyan") + " => " + Colorize(("(private channel)" if msg.channel.is_private else (msg.channel.server.name + "/" + msg.channel.name)), "green") + ": "
	tab = "".join([" " for _ in range(len(metadata))])
	print(metadata + ("(Non-text message or file)" if not msg.content else RemoveUnicode(msg.content).replace("\n", "\n" + tab)))

async def LogMessageEdit(before, after):
	metadata = Colorize("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]", "black") + " " + Colorize(before.author.name, "cyan") + " /> " + Colorize(("(private channel)" if before.channel.is_private else (before.channel.server.name + "/" + before.channel.name)), "green") + ": "
	tab = "".join([" " for _ in range(len(metadata))])
	print(metadata + ("(Non-text message or file)" if not before.content else RemoveUnicode(before.content).replace("\n", "\n" + tab)))
	print(tab[:-3] + "└> ", end="")
	print("(Non-text message or file)" if not after.content else RemoveUnicode(after.content).replace("\n", "\n" + tab))

async def LogMessageDelete(msg):
	metadata = Colorize("[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]", "black") + " " + Colorize(msg.author.name, "cyan") + "? x> " + Colorize(("(private channel)" if msg.channel.is_private else (msg.channel.server.name + "/" + msg.channel.name)), "green") + ": "
	tab = "".join([" " for _ in range(len(metadata))])
	print(metadata + ("(Non-text message or file)" if not msg.content else RemoveUnicode(msg.content).replace("\n", "\n" + tab)))

def NewDimensions(width, height, angle):
	a = abs(width * sin(angle)) + abs(height * cos(angle))
	b = abs(width * cos(angle)) + abs(height * sin(angle))
	return (int(ceil(a)), int(ceil(b)))

def RotateImage(sourceLocation, angle):
	source = Image.open(sourceLocation)
	od = (int(ceil(source.size[0])), int(ceil(source.size[1])))
	nd = NewDimensions(od[0], od[1], angle)
	result = Image.new("RGBA", nd)
	result.paste(source, (ceil((nd[0] - od[0])/2), ceil((nd[1] - od[1])/2)))
	result = result.rotate(angle)
	result.save("pics/temp/temp.png")

def GetPingText(self, msg, tag):
	response = msg.author.mention  + " pinging "
	for userId in self.tags.db[tag]:
		user = FindUserById(msg.channel.server.members, userId)
		if user is not None:
			if user != msg.author:
				response += "[" + (user.mention if user.status != discord.Status.offline else user.name) + "] "
	response += "for " + self.tags.converter[tag]
	return response

def GetConfig(file):
	with open("db/config/" + file + ".json", "r") as f:
		return json.load(f)

def GetConfigAttribute(file, attribute):
	with open("db/config/" + file + ".json", "r") as f:
		return json.load(f)[attribute]

def SaveConfig(file, dict):
	with open("db/config/" + file + ".json", "w") as f:
		json.dump(dict, f)

def SaveConfigAttribute(file, attribute, value):
	with open("db/config/" + file + ".json", "r") as f:
		data = json.load(f)

	data[attribute] = value

	with open("db/config/" + file + ".json", "w") as f:
		json.dump(data, f, indent=4)

def DeleteConfigAttribute(file, attribute):
	with open("db/config/" + file + ".json", "r") as f:
		data = json.load(f)

	del data[attribute]

	with open("db/config/" + file + ".json", "w") as f:
		json.dump(data, f, indent=4)

def Colorize(text, color):
	colors = { "black": 30, "red": 31, "green": 32, "yellow": 33, "blue": 34, "purple": 35, "cyan": 36, "white": 37 }

	if color in colors:
		color = colors[color]

	return "\033[" + str(color) + "m" + text + "\033[0m"
