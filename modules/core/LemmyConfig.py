# Lemmy's stuff
import LemmyCommands as Lcmds

class LemmyConfig:
	def __init__(self):

		self.symbol = {
			"77041788564545536": "!",   # Better Than Skype
			"157748397502234624": "!",   # No Chris Meme Server
			None: "!"
		}
		self.radioVoiceChannel = {
			"77041788564545536": "133010408377286656"   # Better Than Skype (Radio)
		}
		self.radioInfoChannel = {
			"77041788564545536": "134272864999178241"   # Better Than Skype (radio)
		}
		self.voiceToText = {
			"77041788564545536": { # Better Than Skype
				"110179496002338816": "77041788564545536", # Everything
				"77050951277486080": "77046593114615808", # CS:GO
				"77306055939325952": "77303335920611328", # League of Legends
				"77683791056863232": "77683668360892416", # tdeacmc
				"113133087004622848": "77937243011944448", # Blizzard
				"139981745586962432": "138973821171400704", # Halo
				"133010408377286656": None, # Radio
				"109171427252404224": None # AFK
			}
		}
		self.textToVoice = {
			"77041788564545536": { # Better Than Skype
			 	"77041788564545536": "110179496002338816", # everything
				"77046593114615808": "77050951277486080", # csgo
				"77303335920611328": "77306055939325952", # leagueoflegends
				"77683668360892416": "77683791056863232", # tdeacmc
				"110624691177177088": None, # lemmybot
				"77937243011944448": "113133087004622848", # blizzard
				"78040207236005888": None, # nintendo
				"78040100348366848": None, # masseffect
				"77557134866264064": None, # announcements
				"134272864999178241": None # radio
			}
		}
		self.cooldown = {
			"emote": 5,
			"sticker": 5
		}
		self.command = {
			"help": {
				"function": Lcmds.help,
				"enabled": True,
				"moderator": False,
				"description": "...Wait, this seems self-referential..."
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
				"enabled": True,
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
				"enabled": True,
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
			"shrug": {
				"function": Lcmds.shrug,
				"enabled": True,
				"moderator": False,
				"description": "Get a Unicode shrug"
			},
			"thisisfine": {
				"function": Lcmds.thisisfine,
				"enabled": True,
				"moderator": False,
				"description": "Confirm that everything is okay"
			},
			"logout": {
				"function": Lcmds.logout,
				"enabled": True,
				"moderator": True,
				"description": "Turn Lemmy off"
			},
			"shutdown": {
				"function": Lcmds.logout,
				"enabled": True,
				"moderator": True,
				"description": "Turn Lemmy off"
			}
		}