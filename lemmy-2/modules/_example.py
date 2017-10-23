from module import Module

class Example(Module):
	info = 'Explains how to write a module for Lemmy'

	def __init__(self, client):
		Module.__init__(self, client)
		# put setup code to run at bot startup here
		# if you don't have anything in particular you can not define __init__ and it'll use the inherited version

	async def on_message(self, message):
		# you can override on_message if your module does something special
		# you can also call self.call_functions or super(Module, self).call_functions if you just want to add extra functionality on top of the usual
		# otherwise, don't define on_message

	cmd_function_usage = [
			'function',
			'function <argument>'
		]
	async def cmd_function(self, message, args, kwargs):
		# do function stuff
		# you can send an error reaction by raising a CommandError (which by default also sends the usage information),
		# send a success reaction by raising a CommandSuccess,
		# or indicate that the caller does not have the right permission with a CommandNotAllowed

		# try to do stuff
		# when a problem is discovered, raise CommandError
		if len(args) == 0:
			await self.client.send_message(message.channel, 'Default message!')
		elif len(args) == 1:
			await self.client.send_message(message.channel, 'You gave the argument: ' + args[0])
		else:
			raise Module.CommandError

# remember to add your module to manifest.json