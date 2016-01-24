import discord
import os
import sys

if __name__ == "__main__":
	client = discord.Client()



	@client.event
	async def on_ready():
		if sys.argv[3] == "``":
			await client.change_status(game=None)
			await client.logout

		#try:
		text = sys.argv[3]
		print(text)
		await client.change_status(game=discord.Game(name=text))
		#except:
			#await client.logout()
		#else:
			#await client.logout()

		print("Changed game.")
	
	print("Attempting to log in.")
	try:
		client.run(sys.argv[1], sys.argv[2])
	except Exception as e:
		print("ERROR logging into Discord! (" + str(e) + ")")
		quit()