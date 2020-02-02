import sys
sys.path.append('..')

from module import Module

class OldLemmyHelp(Module):
	docs = {
		'description': 'Provides help documentation for Old Lemmy commands'
	}

	docs_lemmycoin = {
		'description': 'Performs LemmyCoin-related operations',
		'usage': 'lemmycoin -balance <username> -pay <username> <amount>',
		'examples': [ 'lemmycoin -balance Lemmy', 'lemmycoin -pay Lemmy 6.9' ]
	}
	async def cmd_lemmycoin(self, message, args, kwargs):
		pass

	docs_restart = {
		'description': 'Restarts Lemmy',
		'admin_only': True
	}
	async def cmd_restart(self, message, args, kwargs):
		pass
