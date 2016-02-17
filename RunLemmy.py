import logging
logging.basicConfig(level=logging.INFO)

import LemmyBot
import datetime

with open("credentials.txt") as f:
	username = f.readline().strip()
	password = f.readline().strip()

lemmy = LemmyBot.LemmyBot(username, password)
input("Lemmy run aborted. Time: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".")