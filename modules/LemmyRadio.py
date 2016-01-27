import discord
import asyncio
import os
from pprint import pprint
import random
import stagger

def GetSongInfo(filename):
		try:
			tag = stagger.read_tag(filename)
		except:
			return None
		else:
			ret = "" + tag.title + "\n"
			ret += "*" + tag.artist + "*\n"
			ret += "*" + tag.album + "*"
			return ret

class Song:
	def __init__(self, player, info):
		self.player = player
		self.info = info

class LemmyRadio:
	def __init__(self, radioChannel, infoChannel):
		self.radioChannel = radioChannel
		self.infoChannel = infoChannel
		self.voiceConnection = None
		self.player = None

	async def ClosePlayer(self):
		if self.player is not None:
			self.player.stop()
			self.player = None

	async def ShuffleTag(self, client, tag):
		directory = "N:\\" + tag + "\\"

		#print("Shuffling " + directory)

		songs = []
		for path, subdirs, files in os.walk(directory):
			for name in files:
				if name.endswith(".mp3") or name.endswith(".m4a"):
					songs.append(os.path.join(path, name))
		random.shuffle(songs)

		#print(str(len(songs)) + " songs in queue.")
		await client.send_message(self.infoChannel, str(len(songs)) + " songs in queue.")

		await self.ClosePlayer()

		while len(songs) > 0 and (self.player is None or self.player.is_done()):
			self.ClosePlayer()

			index = random.randint(0, len(songs) - 1)
			song = songs[index]
			del songs[index]

			self.player = self.voiceConnection.create_ffmpeg_player(song)
			self.player.start()
			info = GetSongInfo(song)
			await client.send_message(self.infoChannel, "**=== Now Playing ===**\n" + info)

	async def PlayYoutubeVideo(self, client, url):
		await self.ClosePlayer()

		self.player = self.voiceConnection.create_ytdl_player(url)
		self.player.start()


			















"""
import sys
sys.path.append('..')

import LemmyUtils as Lutils

import asyncio
import queue
import random
import os
import stagger
from stagger.id3 import *

class LemmyRadio:
	def __init__(self):
		self.currentSong = None
		self.queue = queue.Queue()
		self.radioChannel = None
		self.infoChannel = None
		self.voiceConnection = None
		self.player = None

	### Mutators/Accessors ###

	def SetRadioChannel(self, radioChannel):
		self.radioChannel = radioChannel

	def GetRadioChannel(self):
		return self.radioChannel

	def SetInfoChannel(self, infoChannel):
		self.infoChannel = infoChannel

	def GetInfoChannel(self):
		return self.infoChannel

	def SetVoiceConnection(self, voiceConnection):
		self.voiceConnection = voiceConnection

	### Basic Functions ###

	def StartPlayer(self):
		self.player.start()

	def StopPlayer(self):
		self.player.stop()
		#self.currentSong = None

	def PausePlayer(self):
		self.player.pause()

	def ResumePlayer(self):
		self.player.resume()

	def IsDone(self):
		return self.player.is_done()

	def IsPlaying(self):
		return self.player.is_playing()

	### Other Functions ###

	# Add the file path and name of a local file to queue
	def QueueLocalFile(self, filename):
		print("Queueing " + Lutils.StripUnicode(filename))
		self.queue.put(filename)

	# Add the file path and name of all local files in directory (recursive) to queue
	def QueueDirectory(self, directory):
		for path, subdirs, files in os.walk(directory):
			for name in files:
				if not (name.endswith(".jpg") or name.endswith(".png") or name.endswith(".db")):
					self.QueueLocalFile(path + "\\" + name)

	# Create a Player with a given song
	def LoadSongFromFile(self, filename):
		self.player = self.voiceConnection.create_ffmpeg_player(filename)#, after=self.StartNextOrStop)
		#self.currentSong = filename

	# Create a Player with the next song in queue
	def LoadNextSong(self):
		if not self.queue.empty():
			self.LoadSongFromFile(self.queue.get())

	# Create a Player with the next song in queue and start playing it
	def StartNextSong(self):
		if not self.queue.empty():
			self.LoadSongFromFile(self.queue.get())
			self.player.start()

	# Randomize the order of all items in queue
	def ShuffleQueue(self):
		queue = []
		while not self.queue.empty():
			queue.append(self.queue.get())
		random.shuffle(queue)
		while len(queue) > 0:
			self.queue.put(queue[0])
			del queue[0]

	def ViewQueue(self):
		ret = ""
		queue = []
		while not self.queue.empty():
			queue.append(self.queue.get())
		for song in queue:
			ret += song + "\n"
		while len(queue) > 0:
			self.queue.put(queue[0])
			del queue[0]
		return ret

	# Create a version of ViewQueue that breaks it up into 2000 char chunks

	def ClearQueue(self):
		self.queue = queue.Queue()

	def GetSongInfo(self, filename):
		try:
			tag = stagger.read_tag(filename)
		except:
			return None
		else:
			ret = "**" + tag.title + "**\n"
			ret += "" + tag.artist + "\n"
			ret += "*" + tag.album + "*"
			return ret

	def GetCurrentSong(self):
		#return ":musical_note: Now Playing\n" + (self.GetSongInfo(self.currentSong) if self.currentSong is not None else None)
		if self.currentSong is not None:
			return "--------------\n:musical_note: Now Playing\n" + self.GetSongInfo(self.currentSong)
		else:
			return "No song playing."
"""