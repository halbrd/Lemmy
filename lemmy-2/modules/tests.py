from module import Module

class Tests(Module):
    info = 'Tests features of lemmy-2'

    cmd_send_error_usage = [ 'example 1', 'example 2' ]
    async def cmd_send_error(self, message, args):
        return 'usage'

    cmd_send_success_usage = [ 'example' ]
    async def cmd_send_success(self, message, args):
        return 'success'