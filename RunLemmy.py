import logging
logging.basicConfig(level=logging.INFO)

username = "halbrd@outlook.com"

import LemmyBot

password = input("Enter password\n> ")

lemmy = LemmyBot.LemmyBot(username, password)
lemmy.Start()
input("Lemmy run aborted.")