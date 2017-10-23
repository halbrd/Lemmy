from module import Module

class Lenny(Module):
	info = 'Posts Lenny'

	cmd_lenny_usage = [ 'lenny' ]
	async def cmd_lenny(self, message, args, kwargs):
		await self.client.send_message(message.channel, '( ͡° ͜ʖ ͡°)')
