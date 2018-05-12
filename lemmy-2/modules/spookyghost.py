import sys
sys.path.append('..')
from module import Module

class SpookyGhost(Module):
	async def on_message(self, message):
		if str(message.author.status) == 'offline':
			await self.client.add_reaction(message, '👻')
