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
	async def cmd_function(self, message, args):
		# do function stuff,
		# then return an exit code:
		#   None = all good
		#   'usage' = function was called improperly
		#   'success' = whatever the function was supposed to do was successfully done; no specific response required

		# try to do stuff
		# when a problem is discovered, return 'usage'

		if len(args) == 0:
			await self.client.send_message(message.channel, 'Default message!')
		elif len(args) == 1:
			await self.client.send_message(message.channel, 'You gave the argument: ' + args[0])
		else:
			return 'usage'

# remember to add your module to manifest.json