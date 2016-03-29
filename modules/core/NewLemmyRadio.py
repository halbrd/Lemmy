from enum import Enum
import youtube_dl
import os

class VoiceState(Enum):
	Nothing = 0
	Connected = 1
	Playing = 2

class SongType(Enum):
	Local = 0
	Youtube = 1

class Song:
	def __init__(self, type, location):
		self.type = type # For now, only use Youtube songs
		self.location = location

class LemmyRadio:
	def __init__(self, client):
		self.client = client
		self.voice = None
		self.player = None
		self.youtube_dlOptions = {
			'format': 'bestaudio/best',
			'extractaudio': True,
			'audioformat': "mp3",
			'outtmpl': '%(id)s',
			'noplaylist': True,
			'nocheckcertificate': True,
			'ignoreerrors': True,
			'quiet': True,
			'no_warnings': True,
			'outtmpl': "db/cache/%(id)s"
		}

	async def Connect(self, channel):
		self.voice = self.client.join_voice_channel(channel)

	async def PlaySong(self, song):
		if song.type == SongType.Youtube:
			if self.GetVoiceState() == VoiceState.Playing:
				self.player.stop()
			if self.GetVoiceState() != VoiceState.Connected:
				pass
			songDirectory = self.GetSong(song)
			self.player = client.create_ffmpeg_player(songDirectory)
			self.player.start()
		elif song.type == SongType.Local:
			pass

	async def Pause(self):
		if self.GetVoiceState() == VoiceState.Playing:
			self.player.pause()

	async def Resume(self):
		if self.GetVoiceState() == VoiceState.Playing:
			self.player.resume()

	async def Stop(self):
		if self.GetVoiceState() == VoiceState.Playing:
			self.player.stop()

	def GetVoiceState(self):
		r = None
		if self.voice is None:
			r = VoiceState.Nothing
		elif self.player is None:
			r = VoiceState.Connected
		elif self.player.is_playing():
			r = VoiceState.Playing
		return r


	def GetSong(self, song):
		if song.type == SongType.Youtube:
			ytdl = youtube_dl.YoutubeDL(self.youtube_dlOptions)
			videoData = ytdl.extract_info(song.location, download=False)
			if not os.path.isfile("db/cache/" + videoData["id"]):
				videoData = ytdl.extract_info(song.location, download=True)
			return "db/cache/" + videoData["id"]
		elif song.type == SongType.Local:
			return None