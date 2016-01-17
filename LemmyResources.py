# Lemmy's stuff
import LemmyUtils as Lutils
from LemmyRadio import LemmyRadio

# Other stuff
import os
from os import listdir
from os.path import isfile, join
import json
import sqlite3

class LemmyResources:
	def __init__(self):
		self.lenny = None
		self.lennies = None
		self.emotes = None
		self.stickers = None
		self.jamesDb = None
		self.jamesConverter = None
		self.voiceToTextChannelMap = None
		self.textToVoiceChannelMap = None
		self.sqlConnection = None


	def Load(self):
		print(Lutils.TitleBox("Loading Resources"))
		
		self.lenny = "( ͡° ͜ʖ ͡°)"
		print("Loaded Lenny.")
	
		self.lennies = ["""░░░░░░░░░░░░▄▄▄▄░░░░░░░░░░░░░░░░░░░░░░░▄▄▄▄▄
░░░█░░░░▄▀█▀▀▄░░▀▀▀▄░░░░▐█░░░░░░░░░▄▀█▀▀▄░░░▀█▄
░░█░░░░▀░▐▌░░▐▌░░░░░▀░░░▐█░░░░░░░░▀░▐▌░░▐▌░░░░█▀
░▐▌░░░░░░░▀▄▄▀░░░░░░░░░░▐█▄▄░░░░░░░░░▀▄▄▀░░░░░▐▌
░█░░░░░░░░░░░░░░░░░░░░░░░░░▀█░░░░░░░░░░░░░░░░░░█
▐█░░░░░░░░░░░░░░░░░░░░░░░░░░█▌░░░░░░░░░░░░░░░░░█
▐█░░░░░░░░░░░░░░░░░░░░░░░░░░█▌░░░░░░░░░░░░░░░░░█
░█░░░░░░░░░░░░░░░░░░░░█▄░░░▄█░░░░░░░░░░░░░░░░░░█
░▐▌░░░░░░░░░░░░░░░░░░░░▀███▀░░░░░░░░░░░░░░░░░░▐▌
░░█░░░░░░░░░░░░░░░░░▀▄░░░░░░░░░░▄▀░░░░░░░░░░░░█
░░░█░░░░░░░░░░░░░░░░░░▀▄▄▄▄▄▄▄▀▀░░░░░░░░░░░░░█""", "ヽ( ͡° ͜ʖ ͡°)ﾉ", "( ͡° ͜ʖ ͡°)", "( ͠° ͟ʖ ͡°)", "ᕦ( ͡° ͜ʖ ͡°)ᕤ", "( ͡~ ͜ʖ ͡°)", "( ͡o ͜ʖ ͡o)", "͡° ͜ʖ ͡ -", "( ͡͡ ° ͜ ʖ ͡ °)﻿", "( ͡ ͡° ͡°  ʖ ͡° ͡°)", "(ง ͠° ͟ل͜ ͡°)ง", "( ͡° ͜ʖ ͡ °)", "(ʖ ͜° ͜ʖ)", "[ ͡° ͜ʖ ͡°]", "( ͡o ͜ʖ ͡o)", "{ ͡• ͜ʖ ͡•}", "( ͡° ͜V ͡°)", "( ͡^ ͜ʖ ͡^)", "( ‾ʖ̫‾)", "( ͡°╭͜ʖ╮͡° )", "ᕦ( ͡°╭͜ʖ╮͡° )ᕤ", "(σ ͟ʖσ)", "( ͡°ل͜ ͡°)", "(⚆ ͜ʖ⚆)", "( ͡°⍘ ͡°)", "(´• ͜ʖ •`)", "(Ȍ ͜ʖȌ)", "(❍⍘❍)", "( ͡°‿‿ ͡°)", "(☞ ͡° ͜ʖ ͡°)☞", "(づ ͡° ͜ʖ ͡°)づ", "(☞๏ ͜ʖ๏)☞", "(   ͡ °   ͜ ʖ   ͡ ° )", "(ಠ ͜ʖ ಠ)", "(    ͡   °    ͜   ʖ    ͡   °   )"]
		print("Loaded " + str(len(self.lennies)) + " Lennies.")

		try:
			self.emotes = [ os.path.splitext(f)[0] for f in listdir("pics/emotes") if isfile(join("pics/emotes",f)) ]
		except Exception as e:
			print("ERROR loading emotes! (" + str(e) + ")")
		else:
			print("Loaded " + str(len(self.emotes)) + " emotes.")

		try:
			self.stickers = [ os.path.splitext(f)[0] for f in listdir("pics/stickers") if isfile(join("pics/stickers",f)) ]
		except Exception as e:
			print("ERROR loading stickers! (" + str(e) + ")")
		else:
			print("Loaded " + str(len(self.stickers)) + " stickers.")

		try:
			with open("db/jamesDb.json", "r") as f:
				self.jamesDb = json.load(f)
		except Exception as e:
			print("ERROR loading JamesDb! (" + str(e) + ")")
		else:
			print("JamesDb loaded with " + str(len(self.jamesDb)) + " games.")

		try:
			with open("db/jamesConverter.json", "r") as f:
				self.jamesConverter = json.load(f)
		except Exception as e:
			print("ERROR loading JamesConverter! (" + str(e) + ")")
		else:
			print("JamesConverter loaded with " + str(len(self.jamesConverter)) + " games.")

		try:
			self.sqlConnection = sqlite3.connect("db/sqlite/lemmy.db")
		except Exception as e:
			print("ERROR connecting to database! (" + str(e) + ")")
		else:
			print("Database connection established.")

		self.voiceToTextChannelMaps = {
			"77041788564545536": { # Better Than Skype
				"110179496002338816": "77041788564545536", # Everything
				"77050951277486080": "77046593114615808", # CS:GO
				"77306055939325952": "77303335920611328", # League of Legends
				"77683791056863232": "77683668360892416", # tdeacmc
				"113133087004622848": "77937243011944448", # Blizzard
				"109171427252404224": None # AFK
			}
		}
		print("Voice to text channel map loaded with " + str(len(self.voiceToTextChannelMaps)) + " servers mapped.")

		self.textToVoiceChannelMaps = {
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
		print("Text to voice channel map loaded with " + str(len(self.textToVoiceChannelMaps)) + " servers mapped.")