# Lemmy's stuff
import LemmyUtils as Lutils

# Other stuff
import os
from os import listdir
from os.path import isfile, join
import json
import sqlite3
from ddict import ddict

class LemmyResources:
	def __init__(self):
		self.lenny = None
		self.lennies = None
		self.emotes = None
		self.stickers = None
		self.skype = ddict()
		self.voiceToTextChannelMap = None
		self.textToVoiceChannelMap = None
		self.sqlConnection = None

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
░░░█░░░░░░░░░░░░░░░░░░▀▄▄▄▄▄▄▄▀▀░░░░░░░░░░░░░█""", "ヽ( ͡° ͜ʖ ͡°)ﾉ", "( ͡° ͜ʖ ͡°)", "( ͠° ͟ʖ ͡°)", "ᕦ( ͡° ͜ʖ ͡°)ᕤ", "( ͡~ ͜ʖ ͡°)", "( ͡o ͜ʖ ͡o)", "͡° ͜ʖ ͡ -", "( ͡͡ ° ͜ ʖ ͡ °)﻿", "( ͡ ͡° ͡°  ʖ ͡° ͡°)", "(ง ͠° ͟ل͜ ͡°)ง", "( ͡° ͜ʖ ͡ °)", "(ʖ ͜° ͜ʖ)", "[ ͡° ͜ʖ ͡°]", "( ͡o ͜ʖ ͡o)", "{ ͡• ͜ʖ ͡•}", "( ͡° ͜V ͡°)", "( ͡^ ͜ʖ ͡^)", "( ‾ʖ̫‾)", "( ͡°╭͜ʖ╮͡° )", "ᕦ( ͡°╭͜ʖ╮͡° )ᕤ", "(σ ͟ʖσ)", "( ͡°ل͜ ͡°)", "(⚆ ͜ʖ⚆)", "( ͡°⍘ ͡°)", "(´• ͜ʖ •`)", "(Ȍ ͜ʖȌ)", "(❍⍘❍)", "( ͡°‿‿ ͡°)", "(☞ ͡° ͜ʖ ͡°)☞", "(づ ͡° ͜ʖ ͡°)づ", "(☞๏ ͜ʖ๏)☞", "(   ͡ °   ͜ ʖ   ͡ ° )", "(ಠ ͜ʖ ಠ)", "(    ͡   °    ͜   ʖ    ͡   °   )", "(╭☞ ͡° ͜ʖ ͡° )╭☞", "https://i.imgur.com/5qAb7gO.png"]
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
			self.skype.emotes = [ os.path.splitext(f)[0] for f in listdir("pics/skype/emotes") if isfile(join("pics/skype/emotes",f)) ]
		except Exception as e:
			print("ERROR loading Skype emotes! (" + str(e) + ")")
		else:
			print("Loaded " + str(len(self.skype.emotes)) + " Skype emotes.")

		self.skype.emoteMatch = ("(" + "|".join(self.skype.emotes) + ")") if self.skype.emotes else None

		try:
			self.skype.flags = [ os.path.splitext(f)[0] for f in listdir("pics/skype/flags") if isfile(join("pics/skype/flags",f)) ]
		except Exception as e:
			print("ERROR loading Skype flags! (" + str(e) + ")")
		else:
			print("Loaded " + str(len(self.skype.flags)) + " Skype flags.")

		self.skype.flagMatch = ("(" + "|".join(self.skype.flags) + ")") if self.skype.flags else None

		try:
			self.sqlConnection = sqlite3.connect("db/sqlite/lemmy.db")
		except Exception as e:
			print("ERROR connecting to database! (" + str(e) + ")")
		else:
			print("Database connection established.")
