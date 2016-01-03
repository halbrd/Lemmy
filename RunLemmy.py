import logging
logging.basicConfig(level=logging.INFO)

import LemmyBot

with open("credentials.txt") as f:
	username = f.readline().strip()
	password = f.readline().strip()

lemmy = LemmyBot.LemmyBot(username, password)
input("Lemmy run aborted.")