from grooveshark import Client
from grooveshark.classes import Radio

import subprocess

client = Client()
client.init()

# for song in client.radio(Radio.GENRE_JAZZ):
# 	print(song)
# 	print(song.stream.url)
# 	input()