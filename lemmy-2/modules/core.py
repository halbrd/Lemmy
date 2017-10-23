from module import Module

class Core(Module):
	info = 'Contains basic bot-related functions'

	cmd_shutdown_usage = [ 'shutdown' ]
	async def cmd_shutdown(self, message, args, kwargs):
		if message.author.id in self.lemmy.config["admin_users"]:
			self.lemmy.log('Shutting down...')
			await self.send_success(message)
			await self.client.logout()
		else:
			raise Module.CommandNotAllowed

	cmd_reload_usage = [ 'reload' ]
	async def cmd_reload(self, message, args, kwargs):
		if message.author.id in self.lemmy.config["admin_users"]:
			self.lemmy.log('Reloading...')

			self.lemmy.load_all()

			self.lemmy.log('Reloaded.')
			await self.send_success(message)
		else:
			raise Module.CommandNotAllowed