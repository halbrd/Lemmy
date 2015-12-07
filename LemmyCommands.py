# Lemmy's stuff
import LemmyUtils as Lutils
import RandomLenny

# Other stuff
import random
import discord
import os
from os import listdir
from os.path import isfile, join

def help(client, res, msg, params):
	client.send_message(msg.channel, "http://lynq.me/lemmy")

def emotes(client, res, msg, params):
	client.send_message(msg.channel, "http://lynq.me/lemmy/#emotes")

def stickers(client, res, msg, params):
	client.send_message(msg.channel, "http://lynq.me/lemmy/#stickers")

def lenny(client, res, msg, params):
	flag = Lutils.GetNthFlag(1, params)
	if flag == None:
		client.send_message(msg.channel, res.lennies[random.randint(0, len(res.lennies)-1)])
	elif flag == "-og":
		client.send_message(msg.channel, res.lenny)
	elif flag == "-r":
		client.send_message(msg.channel, RandomLenny.randomLenny())

def logout(client, res, msg, params):
	print("User with id " + str(msg.author.id) + " attempting to logout.")
	if msg.author.id == "77041679726551040":
		client.send_message(msg.channel, "Shutting down.")
		client.logout()

def refresh(client, res, msg, params):
	refreshedEmotes = [ os.path.splitext(f)[0] for f in listdir("pics/emotes") if isfile(join("pics/emotes",f)) ]
	refreshedStickers = [ os.path.splitext(f)[0] for f in listdir("pics/stickers") if isfile(join("pics/stickers",f)) ]

	newEmotes = [item for item in refreshedEmotes if item not in res.emotes]
	newStickers = [item for item in refreshedStickers if item not in res.stickers]

	res.emotes = refreshedEmotes
	res.stickers = refreshedStickers

	if len(newEmotes) > 0:
		client.send_message(msg.channel, "__**New emotes:**__")

		for emote in newEmotes:
			client.send_message(msg.channel, emote)
			client.send_file(msg.channel, "pics/emotes/" + emote + ".png")

	if len(newStickers) > 0:
		client.send_message(msg.channel, "__**New stickers:**__")

		for sticker in newStickers:
			client.send_message(msg.channel, sticker)
			client.send_file(msg.channel, "pics/stickers/" + sticker + ".png")

	client.delete_message(msg)

def correct(client, res, msg, params):
	client.send_message(msg.channel, "https://youtu.be/OoZN3CAVczs")

def eightball(client, res, msg, params):
	responses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes, definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
	client.send_message(msg.channel, msg.author.mention() + " :8ball: " + responses[random.randint(0, len(responses)-1)])

def userinfo(client, res, msg, params):
	if len(params) > 0:
		username = params[0]
		user = discord.utils.find(lambda m: m.name == username, msg.channel.server.members)
		if user:
			client.send_message(msg.channel, "**Username:** " + user.name + "\n**ID:** " + user.id + "\n**Avatar URL:** " + user.avatar_url())
		else:
			client.send_message(msg.channel, "User not found.")

def channelinfo(client, res, msg, params):
	if len(params) > 0:
		channelName = params[0]
		channel = discord.utils.find(lambda m: m.name == channelName, [x for x in msg.channel.server.channels if x.type == "text"])
		if channel:
			client.send_message(msg.channel, "**Channel name: **" + channel.mention() + "\n**ID: **" + channel.id)
		else:
			client.send_message(msg.channel, "Channel not found.")

def james(client, res, msg, params):
	if len(params) > 0:
		flag = Lutils.GetNthFlag(1, params)
		if flag:
			if flag == "-tags":
				response = "```"
				for key in res.jamesDb:
					response += "\n" + key + " (" + res.jamesConverter[key] + ")"
					for member in res.jamesDb[key]:
						response += "\n> " + member
					response += "\n"
				response += "```"
				client.send_message(msg.channel, response)
		else:
			if params[0] in res.jamesDb:
				response = "Pinging "
				for username in res.jamesDb[params[0]]:
					user = discord.utils.find(lambda m: m.name == username, msg.channel.server.members)
					if user is not None:
						response += user.mention() + " "
				response += "for " + res.jamesConverter[params[0]]
				client.send_message(msg.channel, response)

def happening(client, res, msg, params):
	client.send_message(msg.channel, "https://i.imgur.com/bYGOUHP.gif")