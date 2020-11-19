import sys
sys.path.append('..')
from module import Module

class Radio(Module):
    docs = {
        'description': 'Plays audio in voice channels'
    }

    def get_voice_clients(self):
        return {
            voice_client.guild.id: voice_client
            for voice_client in self.client.voice_clients
        }

    async def cmd_lsvoice(self, message, args, kwargs):
        await message.channel.send(self.get_voice_clients())

    docs_radio_on = {
        # TODO
    }
    async def cmd_radio_on(self, message, args, kwargs):
        if message.author.voice is None or message.author.voice.channel is None:
            await self.send_error(message, 'invoker not in a voice channel')
            return

        voice_clients = self.get_voice_clients()

        if message.guild.id in voice_clients:
            await self.send_error(message, 'already in a voice channel in this server')
            return

        await message.author.voice.channel.connect(timeout=10, reconnect=False)


    docs_radio_off = {
        # TODO
    }
    async def cmd_radio_off(self, message, args, kwargs):
        voice_clients = self.get_voice_clients()

        if not message.guild.id in voice_clients:
            await self.send_error(message, 'not in a voice channel on this server')
            return

        await voice_clients[message.guild.id].disconnect()

    docs_radio_queue = {
        # TODO
    }
    async def cmd_radio_queue(self, message, args, kwargs):
        voice_clients = self.get_voice_clients()
        if not message.guild.id in voice_clients:
            await self.send_error(message, 'no radio in this server')
            return

        empty_queue = '{ "index": null, "tracks": [] }'
        queue = self.load_data('queue_' + str(message.guild.id), default=empty_queue)
        await message.channel.send(self.stringify_queue(queue))

    def stringify_queue(self, queue):
        if len(queue['tracks']) == 0:
            return 'nothing playing right now'

        tracks = []
        for i, track in enumerate(queue['tracks']):
            prefix = '=> ' if queue['index'] == i else '   '
            tracks.append(prefix + track['title'])

        track_list = '\n'.join(tracks)

        return '```\n' + track_list + '\n```'
