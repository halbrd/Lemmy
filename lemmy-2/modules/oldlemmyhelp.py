from module import Module

class OldLemmyHelp(Module):
	docs = {
		'description': 'Provides help documentation for Old Lemmy commands'
	}

	docs_8ball = {
		'description': 'Provides a certified correct answer to your question',
		'usage': '8ball <question>'
	}
	async def cmd_8ball(self, message, args, kwargs):
		pass

	docs_choose = {
		'description': 'Chooses between the given options',
		'usage': 'choose <option> or <option> or ...',
		'examples': [ 'choose go left or go right or stay still' ]
	}
	async def cmd_choose(self, message, args, kwargs):
		pass

	docs_refresh = {
		'description': 'Checks for new emotes and stickers'
	}
	async def cmd_refresh(self, message, args, kwargs):
		pass

	docs_fusion = {
		'description': 'Fuses Pokemon together',
		'usage': 'fusion <first Pokemon> <second Pokemon>',
		'examples': [ 'fusion shellder voltorb' ]
	}
	async def cmd_fusion(self, message, args, kwargs):
		pass

	docs_genjimain = {
		'description': 'Gives an insight into the lives of Genji mains'
	}
	async def cmd_genjimain(self, message, args, kwargs):
		pass

	docs_gifr = {
		'description': 'Returns a random gif according to provided search terms',
		'usage': 'gifr <search term>'
	}
	async def cmd_gifr(self, message, args, kwargs):
		pass

	docs_hero = {
		'description': 'Returns a random Overwatch hero'
	}
	async def cmd_hero(self, message, args, kwargs):
		pass

	docs_lemmycoin = {
		'description': 'Performs LemmyCoin-related operations',
		'usage': 'lemmycoin -balance <username> -pay <username> <amount>',
		'examples': [ 'lemmycoin -balance Lemmy', 'lemmycoin -pay Lemmy 6.9' ]
	}
	async def cmd_lemmycoin(self, message, args, kwargs):
		pass

	docs_lol = {
		'description': 'You can look up items or some shit like that',
		'usage': 'lol -item <item name>'
	}
	async def cmd_lol(self, message, args, kwargs):
		pass

	docs_restart = {
		'description': 'Restarts Lemmy',
		'admin_only': True
	}
	async def cmd_restart(self, message, args, kwargs):
		pass

	docs_ruseman = {
		'description': 'Returns a random expression of rusedness'
	}
	async def cmd_ruseman(self, message, args, kwargs):
		pass

	docs_serverinfo = {
		'description': 'Returns information about the server'
	}
	async def cmd_serverinfo(self, message, args, kwargs):
		pass

	docs_skypeemotes = {
		'description': 'Returns a list of available Skype emotes'
	}
	async def cmd_skypeemotes(self, message, args, kwargs):
		pass

	docs_tilt = {
		'description': 'Tilts an emote',
		'usage': 'tilt emote <amount>',
		'examples': [ 'tilt KappaG', 'tilt Jebaited 180' ]
	}
	async def cmd_tilt(self, message, args, kwargs):
		pass

	docs_userinfo = {
		'description': 'Returns information about a user',
		'usage': 'userinfo <username>',
		'examples': [ 'userinfo Lemmy' ]
	}
	async def cmd_userinfo(self, message, args, kwargs):
		pass
