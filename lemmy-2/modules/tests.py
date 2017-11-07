from module import Module

class Tests(Module):
	docs = {
		'description': 'Tests features of lemmy-2'
	}

	docs_send_error = {
		'description': 'Simulates an error occurring',
		'usage': 'send_error <message>',
		'examples': [ 'send_error', 'send_error \'This is what you did wrong!\'' ]
	}
	async def cmd_send_error(self, message, args, kwargs):
		raise Module.CommandError(args[0] if args else None)

	docs_send_success = {
		'description': 'Simulates an action successfully completing'
	}
	async def cmd_send_success(self, message, args, kwargs):
		raise Module.CommandSuccess

	docs_send_dm = {
		'description': 'Sends a direct message',
		'usage': 'send_dm direct_message <public_message>',
		'examples': [ 'send_error \'This message only goes to the recipient!\'', 'send_error \'This message goes to the command caller\' \'This message goes to the channel\'' ]
	}
	async def cmd_send_dm(self, message, args, kwargs):
		if len(args) == 0:
			raise Module.CommandDM
		elif len(args) == 1:
			raise Module.CommandDM(args[0])
		else:
			raise Module.CommandDM(args[0], args[1])

	docs_channel_type = {
		'description': 'Returns the type of the active channel'
	}
	async def cmd_channel_type(self, message, args, kwargs):
		await self.client.send_message(message.channel, type(message.channel))

	docs_dump_args = {
		'description': 'Returns the args and kwargs parsed from the message',
		'usage': 'dump_args <args> <kwargs>',
		'examples': [ 'dump_args a d=1 b e=2 c f=3' ]
	}
	async def cmd_dump_args(self, message, args, kwargs):
		await self.client.send_message(message.channel, f'args:\n{str(args)}\nkwargs:\n{str(kwargs)}')

	async def cmd_no_docs(self, message, args, kwargs):
		await self.client.send_message(message.channel, 'This command has no docs to test the help text')

	cmd_Tests = {
		'description': 'Tests overlapping module/command names'
	}
	async def cmd_Tests(self, message, args, kwargs):
		await self.client.send_message(message.channel, 'This command has the same name as a module to test the help text')
