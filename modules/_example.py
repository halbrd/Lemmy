import sys
sys.path.append('..')
from module import Module

class Example(Module):
    docs = {
        'description': 'Explains how to write a module for Lemmy'
    }

    def __init__(self, lemmy):
        Module.__init__(self, lemmy)
        # put setup code to run at bot startup here
        # if you don't have anything in particular you can not define __init__ and it'll use the inherited version

    async def on_message(self, message):
        # you can override on_message if your module does something special
        # you can also call self.call_functions or super(Module, self).call_functions if you just want to add extra functionality on top of the usual
        # otherwise, don't define on_message

    docs_function = {
        'description': 'Performs an action',   # explain the function's purpose as succintly as possible
        'usage': 'function kwarg=value <optional_kwarg=other_value> arg <optional_arg>',   # represent how to use the function in a technical way; don't define this if the command is self-explanatory
        'examples': [ 'function', 'function arg', 'function kwarg=value arg' ],   # give as few examples as necessary to adequately show how the function can be used; don't define this if the command is self-explanatory or usage explains it clearly enough
        'admin_only': False   # not necessary to define this unless it's true
    }
    async def cmd_function(self, message, args, kwargs):
        # do function stuff
        # you can send an error reaction by raising a CommandError (which by default also sends the usage information),
        # send a success reaction by raising a CommandSuccess,
        # or indicate that the caller does not have the right permission with a CommandNotAllowed

        # try to do stuff
        # when a problem is discovered, raise CommandError
        if len(args) == 0:
            await message.channel.send('Default message!')
        elif len(args) == 1:
            await message.channel.send('You gave the argument: ' + args[0])
        else:
            raise Module.CommandError

# remember to add your module to contexts.ini
