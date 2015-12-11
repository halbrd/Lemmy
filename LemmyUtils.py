import discord

class DecomposedMessage:
	def __init__(self, command, params):
		self.command = command
		self.params = params

def GetDecomposedMessage(message):
	if message[0] == "!":
		message = message[1:]
	decompArray = message.split()
	decomp = DecomposedMessage(decompArray[0], decompArray[1:])

	return decomp

def GetNthFlag(n, params):
	for i in range(0, len(params)):
		if params[i][0] == "-":
			if n == 1:
				if i + 1 < len(params) and params[i + 1][0] != "-":
					return [params[i], params[i + 1]]
				else:
					return [params[i], None]
			else:
				n -= 1
	return None

def SendEmote(client, msg):
	client.send_message(msg.channel, "__**" + msg.author.name + "**__")
	client.send_file(msg.channel, "pics/emotes/" + msg.content + ".png")
	client.delete_message(msg)

def SendSticker(client, msg):
	client.send_message(msg.channel, "__**" + msg.author.name + "**__")
	client.send_file(msg.channel, "pics/stickers/" + msg.content + ".png")
	client.delete_message(msg)

def StripUnicode(string):
	stripped = [c for c in string if 0 < ord(c) < 127]
	return "".join(stripped)

def IsAdmin(member):
	return "administrator" in [role.name for role in member.roles]

def IsModOrAbove(member):
	return "administrator" in [role.name for role in member.roles] or "moderator" in [role.name for role in member.roles] or "robots" in [role.name for role in member.roles]

def IsRole(role, member):
	return role in [role.name for role in member.roles]

def FindUserByName(members, username):
	return discord.utils.find(lambda m: m.name == username, members)

def FindUserById(members, userId):
	return discord.utils.find(lambda m: m.id == userId, members)