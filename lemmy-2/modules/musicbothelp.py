from module import Module

class MusicBotHelp(Module):
	docs = {
		'description': 'Provides help documentation for MusicBot commands'
	}

	docs_blacklist = {
		'description': 'Adds or removes users to the blacklist'
	}
	async def cmd_blacklist(self, message, args, kwargs):
		pass

	docs_clean = {
		'description': 'Removes messages that the bot has posted in chat'
	}
	async def cmd_clean(self, message, args, kwargs):
		pass

	docs_clear = {
		'description': 'Clears the playlist'
	}
	async def cmd_clear(self, message, args, kwargs):
		pass

	docs_dc = {
		'description': 'Disconnects the bot from the voice channel'
	}
	async def cmd_dc(self, message, args, kwargs):
		pass

	docs_joinserver = {
		'description': 'Asks the bot to join a server'
	}
	async def cmd_joinserver(self, message, args, kwargs):
		pass

	docs_np = {
		'description': 'Prints the current song'
	}
	async def cmd_np(self, message, args, kwargs):
		pass

	docs_pause = {
		'description': 'Pauses playback'
	}
	async def cmd_pause(self, message, args, kwargs):
		pass

	docs_perms = {
		'description': 'Sends the user a list of their permissions'
	}
	async def cmd_perms(self, message, args, kwargs):
		pass

	docs_play = {
		'description': 'Adds a song to the playlist',
		'usage': 'play <Youtube link or search term>',
		'examples': [ 'play https://www.youtube.com/watch?v=KelFDPAPUyY', 'play hotel california' ]
	}
	async def cmd_play(self, message, args, kwargs):
		pass

	docs_pldump = {
		'description': 'Dumps the individual urls of a playlist'
	}
	async def cmd_pldump(self, message, args, kwargs):
		pass

	docs_queue = {
		'description': 'Prints the current song queue'
	}
	async def cmd_queue(self, message, args, kwargs):
		pass

	docs_resume = {
		'description': 'Resumes playback'
	}
	async def cmd_resume(self, message, args, kwargs):
		pass

	docs_search = {
		'description': 'Searches for videos matching a search term and allows the user to select from them',
		'usage': 'search <search term>'
	}
	async def cmd_search(self, message, args, kwargs):
		pass

	docs_setavatar = {
		'description': 'Changes the bot\'s avatar',
		'usage': 'setavatar <url or attached image>',
		'admin_only': True
	}
	async def cmd_setavatar(self, message, args, kwargs):
		pass

	docs_setname = {
		'description': 'Changes the bot\'s username',
		'admin_only': True
	}
	async def cmd_setname(self, message, args, kwargs):
		pass

	docs_setnick = {
		'description': 'Changes the bot\'s nickname',
		'admin_only': True
	}
	async def cmd_setnick(self, message, args, kwargs):
		pass

	docs_shuffle = {
		'description': 'Shuffles the playlist'
	}
	async def cmd_shuffle(self, message, args, kwargs):
		pass

	docs_shutdown = {
		'description': 'Shuts down the bot',
		'admin_only': True
	}
	async def cmd_shutdown(self, message, args, kwargs):
		pass

	docs_skip = {
		'description': 'Skips the current song when enough votes are cast, or by the bot owner'
	}
	async def cmd_skip(self, message, args, kwargs):
		pass

	docs_summon = {
		'description': 'Calls the bot to the summoner\'s voice channel'
	}
	async def cmd_summon(self, message, args, kwargs):
		pass

	docs_volume = {
		'description': 'Sets the playback volume',
		'usage': 'volume <+/-><amount>',
		'examples': [ 'volume 6', 'volume +3', 'volume -1' ]
	}
	async def cmd_volume(self, message, args, kwargs):
		pass
