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

	def Load(self):
		print("\n=====================\n= Loading Resources =\n=====================\n")
		
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
░░░█░░░░░░░░░░░░░░░░░░▀▄▄▄▄▄▄▄▀▀░░░░░░░░░░░░░█""", "ヽ( ͡° ͜ʖ ͡°)ﾉ", "( ͡° ͜ʖ ͡°)", "( ͠° ͟ʖ ͡°)", "ᕦ( ͡° ͜ʖ ͡°)ᕤ", "( ͡~ ͜ʖ ͡°)", "( ͡o ͜ʖ ͡o)", "͡° ͜ʖ ͡ -", "( ͡͡ ° ͜ ʖ ͡ °)﻿", "( ͡ ͡° ͡°  ʖ ͡° ͡°)", "(ง ͠° ͟ل͜ ͡°)ง", "( ͡° ͜ʖ ͡ °)", "(ʖ ͜° ͜ʖ)", "[ ͡° ͜ʖ ͡°]", "( ͡o ͜ʖ ͡o)", "{ ͡• ͜ʖ ͡•}", "( ͡° ͜V ͡°)", "( ͡^ ͜ʖ ͡^)", "( ‾ʖ̫‾)", "( ͡°╭͜ʖ╮͡° )", "ᕦ( ͡°╭͜ʖ╮͡° )ᕤ", "(σ ͟ʖσ)", "( ͡°ل͜ ͡°)", "(⚆ ͜ʖ⚆)", "( ͡°⍘ ͡°)", "(´• ͜ʖ •`)", "(Ȍ ͜ʖȌ)", "(❍⍘❍)", "( ͡°‿‿ ͡°)", "(☞ ͡° ͜ʖ ͡°)☞", "(づ ͡° ͜ʖ ͡°)づ", "(☞๏ ͜ʖ๏)☞", "(   ͡ °   ͜ ʖ   ͡ ° )", "(ಠ ͜ʖ ಠ)"]
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