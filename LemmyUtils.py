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
				return params[i]
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