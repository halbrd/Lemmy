# hmmm
# step 1: extract metadata from individual videos and playlists, given a link to either one
# step 2: cache those videos to disk
# step 3: move Lemmy around through the voice channels comfortably and effectively
# step 4: all automated cleanup
# step 5: queue and play audio


import sys
sys.path.append('..')
from module import Module

import discord
import youtube_dl

class Radio(Module):
    docs = {
        'description': 'Plays audio in voice channels'
    }

    # general management functions

    def get_voice_clients(self):
        return {
            voice_client.guild.id: voice_client
            for voice_client in self.client.voice_clients
        }

    # Youtube functions

    def _extract_video_metadata(self, ytdl_output):
        return {
            'id': ytdl_output['id'],
            'title': ytdl_output['title'],
            'source': ytdl_output['webpage_url'],
        }

    def get_all_videos_metadata(self, url):
        with youtube_dl.YoutubeDL() as ytdl:
            result = ytdl.extract_info(
                url,
                download=False
            )

        if result.get('_type') == 'playlist':
            # it's a playlist
            videos = result['entries']
        else:
            # it's an individual video
            videos = [result]

        return [ self._extract_video_metadata(video) for video in videos ]

    async def cmd_getmeta(self, message, args, kwargs):
        import json
        for url in args:
            data = self.get_all_videos_metadata(url)
            await message.channel.send(f'```\n{json.dumps(data, indent=2)}\n```')

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
