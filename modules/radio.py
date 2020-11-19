import sys
sys.path.append('..')
from module import Module

class Radio(Module):
    docs = {
        'description': 'Plays audio in voice channels'
    }

    def __init__(self, lemmy):
        Module.__init__(self, lemmy)

        # this stores all of the active voice clients
        # it is indexed by server id because each server may only have one voice client
        # [voice_channel.server.id] -> voice_client
        # you can always call voice_client.channel and voice_client.guild
        self.voice_clients = {}

    docs_radio_on = {
        # TODO
    }
    async def cmd_radio_on(self, message, args, kwargs):
        if message.guild.id in self.voice_clients:
            raise Exception('already in a voice channel in this server')

        if message.author.voice is None or message.author.voice.channel is None:
            raise Exception('invoker not in a voice channel')

        voice_client = await message.author.voice.channel.connect(timeout=10, reconnect=False)
        self.voice_clients[voice_client.guild.id] = voice_client


    docs_radio_off = {
        # TODO
    }
    async def cmd_radio_off(self, message, args, kwargs):
        if not message.channel.guild.id in self.voice_clients:
            raise Exception('not in a voice channel on this server')

        await self.voice_clients[message.channel.guild.id].disconnect()
        del self.voice_clients[message.channel.guild.id]
