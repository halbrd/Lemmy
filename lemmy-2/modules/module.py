class Module:
    class CommandError(Exception):
        def __init__(self, message=None):
            if message is None:
                usage = getattr(self, f'cmd_{terms[0]}_usage')
                message = 'Usage:\n' + '\n'.join(['`' + form + '`' for form in usage])

            super(CommandError, self).__init__(message)

    class CommandSuccess(Exception):
        def __init__(self, message=None):   # is this superfluous?
            super(CommandSuccess, self).__init__(message)

    def __init__(self, lemmy):
        self.lemmy = lemmy
        self.client = lemmy.client   # this line is arguably bad taste code, but the name binding removes a *lot* of typing
        self.commands = { function[4:]: getattr(self, function) for function in dir(self) if function.startswith('cmd_') }

    async def on_message(self, message):
        await self.call_functions(message)

    async def call_functions(self, message):
        terms = Module.deconstruct_message(message)

        try:
            symbol = self.lemmy.config_try_key("server_config", message.channel.server.id, "symbol")
        except ( AttributeError, KeyError ):
            symbol = self.lemmy.config["default_symbol"]

        if len(terms) > 0 and terms[0].startswith(symbol):
            terms[0] = terms[0][len(symbol):]

            if terms[0] in self.commands:
                try:
                    await self.commands[terms[0]](message, terms[1:])
                except CommandError as e:
                    await self.send_error(message, e.message)
                except CommandSuccess as e:
                    await self.send_success(message, e.message)

    @staticmethod
    def deconstruct_message(message):
        # TODO: preserve quoted sections
        return message.content.split()

    async def send_error(self, message, comment=None):
        await self.client.add_reaction(message, '❌')

        if comment:
            await self.client.send_message(message.channel, comment)

    async def send_success(self, message, comment=None):
        await self.client.add_reaction(message, '✅')

        if comment:
            await self.client.send_message(message.channel, comment)