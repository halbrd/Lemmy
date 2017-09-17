class Module:
    def __init__(self, client):
        self.client = client
        self.commands = { function[4:]: getattr(self, function) for function in dir(self) if function.startswith('cmd_') }

    async def on_message(self, message):
        await self.call_functions(message)

    async def call_functions(self, message):
        terms = Module.deconstruct_message(message)

        if terms[0] in self.commands:
            exit_code = await self.commands[terms[0]](message, terms[1:])

            # I was really torn over using exit codes or exceptions for this
            # I went with exit codes because otherwise I'd be raising an exception for send_success, which isn't an error condition
            # Python's design paradigms are flexible and I could use an exception for non-error purposes, but it feels dirty and wrong
            # ...somehow less so than string codes...
            if exit_code is None:
                pass
            elif exit_code == 'usage':
                await self.send_error(message, getattr(self, f'cmd_{terms[0]}_usage'))
            elif exit_code == 'success':
                await self.send_success(message)
            else:
                raise ValueError(f'"{exit_code}" is not a valid exit code')


    @staticmethod
    def deconstruct_message(message):
        # this function could be much more complex, but it doesn't need to be more heavily engineered than this
        return message.content.split()

    async def send_error(self, message, usage):
        await self.client.add_reaction(message, '❌')
        await self.client.send_message(message.channel, 'Usage:\n' + '\n'.join(['`' + form + '`' for form in usage]))

    async def send_success(self, message):
        await self.client.add_reaction(message, '✅')