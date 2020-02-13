# Lemmy's stuff
import LemmyCommands as Lcmds

import json

class LemmyConfig:
	def __init__(self):

		with open("db/config/symbol.json",  "r") as f:
			self.symbol = json.load(f)

		with open("db/config/voiceToText.json",  "r") as f:
			self.voiceToText = json.load(f)

		with open("db/config/textToVoice.json",  "r") as f:
			self.textToVoice = json.load(f)

		with open("db/config/cooldown.json",  "r") as f:
			self.cooldown = json.load(f)

		self.command = {
			"help": {
				"function": Lcmds.help,
				"enabled": False,
				"moderator": False,
				"description": "...Wait, this seems self-referential..."
			},
			"restart": {
				"function": Lcmds.logout,
				"enabled": True,
				"moderator": True,
				"description": "Restart Lemmy"
			},
			"lenny": {
				"function": Lcmds.lenny,
				"enabled": False,
				"moderator": False,
				"description": "Get a Lenny"
			},
			"refresh": {
				"function": Lcmds.refresh,
				"enabled": False,
				"moderator": False,
				"description": "Check for new stickers and emotes"
			},
			"f5": {
				"function": Lcmds.refresh,
				"enabled": False,
				"moderator": False,
				"description": "Check for new stickers and emotes"
			},
			"8ball": {
				"function": Lcmds.eightball,
				"enabled": False,
				"moderator": False,
				"description": "Get a certified correct answer to your question"
			},
			"userinfo": {
				"function": Lcmds.userinfo,
				"enabled": False,
				"moderator": False,
				"description": "Get info about a user"
			},
			"ruseman": {
				"function": Lcmds.ruseman,
				"enabled": False,
				"moderator": False,
				"description": "Get a random expression of rusedness"
			},
			"lemmycoin": {
				"function": Lcmds.lemmycoin,
				"enabled": True,
				"moderator": False,
				"description": "Perform LemmyCoin-related operations"
			},
			"lc": {
				"function": Lcmds.lemmycoin,
				"enabled": True,
				"moderator": False,
				"description": "Perform LemmyCoin-related operations"
			},
			"l$": {
				"function": Lcmds.lemmycoin,
				"enabled": True,
				"moderator": False,
				"description": "Perform LemmyCoin-related operations"
			},
			"serverinfo": {
				"function": Lcmds.serverinfo,
				"enabled": False,
				"moderator": False,
				"description": "Get info about the current server"
			},
			"choose": {
				"function": Lcmds.choose,
				"enabled": False,
				"moderator": False,
				"description": "Choose between the given options"
			},
			"tilt": {
				"function": Lcmds.tilt,
				"enabled": False,
				"moderator": False,
				"description": "Get a rotated emote"
			},
			"skypeemotes": {
				"function": Lcmds.skypeemotes,
				"enabled": False,
				"moderator": False,
				"description": "Get a list of Skype emotes"
			},
			"lol": {
				"function": Lcmds.lol,
				"enabled": True,
				"moderator": False,
				"description": "You can look up items or some shit like that"
			},
			"ccomm": {
				"function": Lcmds.ccomm,
				"enabled": False,
				"moderator": False,
				"description": "Manage custom commands"
			},
			"hero": {
				"function": Lcmds.hero,
				"enabled": True,
				"moderator": False,
				"description": "Choose a random Overwatch hero"
			},
			"genjimain": {
				"function": Lcmds.genjimain,
				"enabled": False,
				"moderator": False,
				"description": "Get an insight into the lives of Genji players"
			},
			"gifr": {
				"function": Lcmds.gifr,
				"enabled": True,
				"moderator": False,
				"description": "Get a random gif with search terms"
			},
			"fusion": {
				"function": Lcmds.fusion,
				"enabled": False,
				"moderator": False,
				"description": "Get a Pokemon fusion"
			}
		}
