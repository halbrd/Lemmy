#!/usr/bin/python3.5

import logging
logging.basicConfig(level=logging.INFO)

import LemmyBot
import datetime
import time

#while True:
with open("credentials.txt") as f:
	#username = f.readline().strip()
	#password = f.readline().strip()
	token = f.readline().strip()

lemmy = LemmyBot.LemmyBot(token)
print("Lemmy run aborted. Time: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".")