from module import Module

class Core(Module):
    info = 'Contains basic bot-related functions'

    cmd_shutdown_usage = [ 'shutdown' ]
    async def cmd_shutdown(self, message, args):

        if message.author.id in self.lemmy.config["admin_users"]:
            await self.send_success(message)
            await self.client.logout()

