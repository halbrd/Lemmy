from module import Module

class Tests(Module):
	info = 'Tests features of lemmy-2'

	cmd_send_error_usage = [ 'send_error', 'send_error <message>' ]
	async def cmd_send_error(self, message, args, kwargs):
		raise Module.CommandError(args[0] if args else None)

	cmd_send_success_usage = [ 'example' ]
	async def cmd_send_success(self, message, args, kwargs):
		raise Module.CommandSuccess

	cmd_channel_type_usage = [ 'channel_type' ]
	async def cmd_channel_type(self, message, args, kwargs):
		await self.client.send_message(message.channel, type(message.channel))

	cmd_dump_args_usage = [ 'I can\'t be bothered writing this' ]
	async def cmd_dump_args(self, message, args, kwargs):
		await self.client.send_message(message.channel, f'args:\n{str(args)}\nkwargs:\n{str(kwargs)}')