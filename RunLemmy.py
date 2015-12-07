username = "halbrd@outlook.com"

from LemmyBot import LemmyBot

password = input("Enter password\n> ")
lemmy = LemmyBot(username, password)
lemmy.Start()