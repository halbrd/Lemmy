import logging
logging.basicConfig(level=logging.INFO)

import LemmyBot
import datetime

while True:
	with open("credentials.txt") as f:
		username = f.readline().strip()
		password = f.readline().strip()

	lemmy = LemmyBot.LemmyBot(username, password)
	print("Lemmy run aborted. Time: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".")