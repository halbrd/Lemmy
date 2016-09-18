import sys
sys.path.append('system/core')
sys.path.append('system/modules')

from LemmyUtils import *

import discord
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
	print("Logged in as " + bot.user.name + " | " + bot.user.id)

@bot.event
async def on_message(message):
	print(message.content)

@bot.command()
async def addT(left : int, right : int):
	await bot.say(left + right)

@bot.command()
async def addF(left, right):
	await bot.say(left + right)

def main():
	loginInfo = JsonGet(JsonPath["login"])
	if loginInfo["token"] != "":
		yield from bot.login(loginInfo["token"])
	else:
		yield from bot.login(loginInfo["email"], loginInfo["password"])
	yield from bot.connect()

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(main())
	except Exception as e:
		print(e)
		loop.run_until_complete(bot.logout())
	finally:
		loop.close()