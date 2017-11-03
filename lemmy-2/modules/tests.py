from module import Module
import asyncio

class Tests(Module):
	info = 'Tests features of lemmy-2'

	cmd_send_error_usage = [ 'send_error', 'send_error <message>' ]
	async def cmd_send_error(self, message, args, kwargs):
		raise Module.CommandError(args[0] if args else None)

	cmd_send_success_usage = [ 'example' ]
	async def cmd_send_success(self, message, args, kwargs):
		raise Module.CommandSuccess

	cmd_send_not_allowed_usage = [ 'send_not_allowed' ]
	async def cmd_send_not_allowed(self, message, args, kwargs):
		raise Module.CommandNotAllowed

	cmd_send_dm_usage = [ 'send_dm direct_message <public_message>' ]
	async def cmd_send_dm(self, message, args, kwargs):
		if len(args) == 0:
			raise Module.CommandDM
		elif len(args) == 1:
			raise Module.CommandDM(args[0])
		else:
			raise Module.CommandDM(args[0], args[1])

	cmd_channel_type_usage = [ 'channel_type' ]
	async def cmd_channel_type(self, message, args, kwargs):
		await self.client.send_message(message.channel, type(message.channel))

	cmd_dump_args_usage = [ 'I can\'t be bothered writing this' ]
	async def cmd_dump_args(self, message, args, kwargs):
		await self.client.send_message(message.channel, f'args:\n{str(args)}\nkwargs:\n{str(kwargs)}')

	cmd_react_usage = [ 'react <emojis>' ]
	async def cmd_react(self, message, args, kwargs):
		loop = asyncio.get_event_loop()
		for emoji in args:
			# holy crap, this naturally works synchronously?
			await self.client.add_reaction(message, emoji)