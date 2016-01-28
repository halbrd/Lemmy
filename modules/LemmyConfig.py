# Lemmy's stuff
import LemmyCommands as Lcmds

class LemmyConfig:
	def __init__(self):
		self.symbol = {
			"77041788564545536": "!",   # Better Than Skype
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
				"moderator": False
			},
			"emotes": {
				"function": Lcmds.emotes,
				"enabled": True,
				"moderator": False
			},
			"stickers": {
				"function": Lcmds.stickers,
				"enabled": True,
				"moderator": False
			},
			"lenny": {
				"function": Lcmds.lenny,
				"enabled": True,
				"moderator": False
			},
			"refresh": {
				"function": Lcmds.refresh,
				"enabled": True,
				"moderator": False
			},
			"f5": {
				"function": Lcmds.refresh,
				"enabled": True,
				"moderator": False
			},
			"correct": {
				"function": Lcmds.correct,
				"enabled": True,
				"moderator": False
			},		
			"8ball": {
				"function": Lcmds.eightball,
				"enabled": True,
				"moderator": False
			},
			"userinfo": {
				"function": Lcmds.userinfo,
				"enabled": True,
				"moderator": False
			},
			"channelinfo": {
				"function": Lcmds.channelinfo,
				"enabled": True,
				"moderator": False
			},
			"james": {
				"function": Lcmds.james,
				"enabled": True,
				"moderator": False
			},
			"happening": {
				"function": Lcmds.happening,
				"enabled": True,
				"moderator": False
			},
			"ruseman": {
				"function": Lcmds.ruseman,
				"enabled": True,
				"moderator": False
			},
			"lemmycoin": {
				"function": Lcmds.lemmycoin,
				"enabled": True,
				"moderator": False
			},
			"lc": {
				"function": Lcmds.lemmycoin,
				"enabled": True,
				"moderator": False
			},
			"l$": {
				"function": Lcmds.lemmycoin,
				"enabled": True,
				"moderator": False
			},
			"channelids": {
				"function": Lcmds.channelids,
				"enabled": True,
				"moderator": False
			},
			"serverinfo": {
				"function": Lcmds.serverinfo,
				"enabled": True,
				"moderator": False
			},
			"choose": {
				"function": Lcmds.choose,
				"enabled": True,
				"moderator": False
			},
			"radio": {
				"function": Lcmds.radio,
				"enabled": True,
				"moderator": False
			},
			"tts": {
				"function": Lcmds.tts,
				"enabled": False,
				"moderator": False
			},
			"playgame": {
				"function": Lcmds.playgame,
				"enabled": True,
				"moderator": False
			},
			"tilt": {
				"function": Lcmds.tilt,
				"enabled": True,
				"moderator": False
			},
			"logout": {
				"function": Lcmds.logout,
				"enabled": True,
				"moderator": True
			},
			"shutdown": {
				"function": Lcmds.logout,
				"enabled": True,
				"moderator": True
			}
		}