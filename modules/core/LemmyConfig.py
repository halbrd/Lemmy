# Lemmy's stuff
import LemmyCommands as Lcmds

import json

class LemmyConfig:
	def __init__(self):

		with open("db/config/symbol.json",  "r") as f:
			self.symbol = json.load(f)

		with open("db/config/radioVoiceChannel.json",  "r") as f:
			self.radioVoiceChannel = json.load(f)

		with open("db/config/radioInfoChannel.json",  "r") as f:
			self.radioInfoChannel = json.load(f)

		with open("db/config/voiceToText.json",  "r") as f:
			self.voiceToText = json.load(f)

		with open("db/config/textToVoice.json",  "r") as f:
			self.textToVoice = json.load(f)

		with open("db/config/cooldown.json",  "r") as f:
			self.cooldown = json.load(f)

		self.command = {
			"help": {
				"function": Lcmds.help,
				"enabled": True,
				"moderator": False,
				"description": "...Wait, this seems self-referential..."
			},
			"restart": {
				"function": Lcmds.logout,
				"enabled": True,
				"moderator": True,
				"description": "Turn Lemmy off"
			},
			"emotes": {
				"function": Lcmds.emotes,
				"enabled": True,
				"moderator": False,
				"description": "Get a list of emotes"
			},
			"stickers": {
				"function": Lcmds.stickers,
				"enabled": True,
				"moderator": False,
				"description": "Get a list of stickers"
			},
			"lenny": {
				"function": Lcmds.lenny,
				"enabled": True,
				"moderator": False,
				"description": "Get a Lenny"
			},
			"refresh": {
				"function": Lcmds.refresh,
				"enabled": True,
				"moderator": False,
				"description": "Check for new stickers and emotes"
			},
			"f5": {
				"function": Lcmds.refresh,
				"enabled": True,
				"moderator": False,
				"description": "Check for new stickers and emotes"
			},
			"correct": {
				"function": Lcmds.correct,
				"enabled": False,
				"moderator": False,
				"description": "Get the correct horse video"
			},
			"8ball": {
				"function": Lcmds.eightball,
				"enabled": True,
				"moderator": False,
				"description": "Get a certified correct answer to your question"
			},
			"userinfo": {
				"function": Lcmds.userinfo,
				"enabled": True,
				"moderator": False,
				"description": "Get info about a user"
			},
			"channelinfo": {
				"function": Lcmds.channelinfo,
				"enabled": True,
				"moderator": False,
				"description": "Get info about a channel"
			},
			"james": {
				"function": Lcmds.james,
				"enabled": True,
				"moderator": False,
				"description": "Perform tag-related operations"
			},
			"happening": {
				"function": Lcmds.happening,
				"enabled": False,
				"moderator": False,
				"description": "Get a high quality Ron Paul gif"
			},
			"ruseman": {
				"function": Lcmds.ruseman,
				"enabled": True,
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
			"channelids": {
				"function": Lcmds.channelids,
				"enabled": True,
				"moderator": False,
				"description": "Get a list of channel ids on the current server"
			},
			"serverinfo": {
				"function": Lcmds.serverinfo,
				"enabled": True,
				"moderator": False,
				"description": "Get info about the current server"
			},
			"choose": {
				"function": Lcmds.choose,
				"enabled": True,
				"moderator": False,
				"description": "Choose between the given options"
			},
			"radio": {
				"function": Lcmds.radio,
				"enabled": True,
				"moderator": False,
				"description": "Perform radio-related operations"
			},
			"tts": {
				"function": Lcmds.tts,
				"enabled": False,
				"moderator": False,
				"description": "Make Lemmy say the given message"
			},
			"playgame": {
				"function": Lcmds.playgame,
				"enabled": True,
				"moderator": False,
				"description": "Set Lemmy's \"Playing\" message"
			},
			"tilt": {
				"function": Lcmds.tilt,
				"enabled": True,
				"moderator": False,
				"description": "Get a rotated emote"
			},
			"skypeemotes": {
				"function": Lcmds.skypeemotes,
				"enabled": True,
				"moderator": False,
				"description": "Get a list of Skype emotes"
			},
			"thisisfine": {
				"function": Lcmds.thisisfine,
				"enabled": False,
				"moderator": False,
				"description": "Confirm that everything is okay"
			},
			"role": {
				"function": Lcmds.role,
				"enabled": True,
				"moderator": False,
				"description": "Manage role membership"
			},
			"lol": {
				"function": Lcmds.lol,
				"enabled": True,
				"moderator": False,
				"description": "You can look up items or some shit like that"
			},
			"joinlink": {
				"function": Lcmds.joinlink,
				"enabled": True,
				"moderator": False,
				"description": "Get link to invite Lemmy to other servers"
			},
			"leave": {
				"function": Lcmds.leave,
				"enabled": True,
				"moderator": False,
				"description": "Remove Lemmy from server"
			},
			"ccomm": {
				"function": Lcmds.ccomm,
				"enabled": True,
				"moderator": False,
				"description": "Manage custom commands"
			},
			"coinflip": {
				"function": Lcmds.coinflip,
				"enabled": True,
				"moderator": False,
				"description": "Flip a coin"
			},
			"emoji": {
				"function": Lcmds.emoji,
				"enabled": True,
				"moderator": True,
				"description": "Manage server emojis"
			},
			"resetprofile": {
				"function": Lcmds.resetprofile,
				"enabled": True,
				"moderator": True,
				"description": "laters"
			},
			"hero": {
				"function": Lcmds.hero,
				"enabled": True,
				"moderator": False,
				"description": "Choose a random Overwatch hero"
			},
			"rainbow": {
				"function": Lcmds.rainbow,
				"enabled": False,
				"moderator": False,
				"description": "Make a role rainbow"
			},
			"genjimain": {
				"function": Lcmds.genjimain,
				"enabled": True,
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
				"enabled": True,
				"moderator": False,
				"description": "Get a Pokemon fusion"
			},
			"roll": {
				"function": Lcmds.roll,
				"enabled": True,
				"moderator": False,
				"description": "Roll D&D dice (eg. 2d20kh)"
			},
			"gifembedtest": {
				"function": Lcmds.gifembedtest,
				"enabled": True,
				"moderator": False,
				"description": ""
			}
		}
