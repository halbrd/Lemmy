import sys
sys.path.append('..')
from module import Module

import discord
import youtube_dl
import os
import shutil
from urllib.parse import urlparse

CACHE_LOC = 'cache/Radio/'

# copied from https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': CACHE_LOC + '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.25):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.filename = data.get('filename')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        data['filename'] = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(data['filename'], **ffmpeg_options), data=data)



class Radio(Module):
    docs = {
        'description': '[Alpha Testing] Plays sound in voice'
    }

    def __init__(self, lemmy):
        Module.__init__(self, lemmy)

        if os.path.exists(CACHE_LOC):
            shutil.rmtree(CACHE_LOC)

        self.queues = {}

    docs_radio_play = {
        'description': 'Plays YouTube videos',
        'usage': 'radio_play youtube_link <youtube_link> ...',
        'examples': [
            'radio_play https://youtu.be/sz2mmM-kN1I',
            'radio_play https://youtu.be/L5nip3WB9lc https://youtu.be/dfyNnUgK8qE'
        ],
    }
    async def cmd_radio_play(self, message, args, kwargs):
        # save a bunch of state variables to make the following code clear
        lemmy_voice = message.guild.voice_client
        user_voice = message.author.voice

        lemmy_in_voice = lemmy_voice is not None
        user_in_voice = user_voice is not None
        user_with_lemmy = lemmy_in_voice and user_in_voice and user_voice.channel == lemmy_voice.channel

        # preflight checks - input
        if len(args) == 0:
            await self.send_error(message)
            return

        for url in args:
            domain = urlparse(url).netloc
            if not domain in ['youtube.com', 'www.youtube.com', 'youtu.be']:
                await self.send_error(message, comment='Only YouTube videos are supported at this time')
                return

        # preflight checks - voice state
        if not user_in_voice:
            await self.send_error(message, comment='You need to be in a voice channel')
            return

        if lemmy_in_voice and not user_with_lemmy and lemmy_voice.is_playing():
            await self.send_error(message, comment='Radio is already playing in this server')
            return

        # ensure Lemmy is in the right voice place
        if not user_with_lemmy:
            if not lemmy_in_voice:
                await user_voice.channel.connect()
            else:
                await lemmy_voice.move_to(user_voice.channel)

        vc = message.guild.voice_client

        # ensure queue exists
        if not message.guild.id in self.queues:
            self.queues[message.guild.id] = []

        # add the given video to queue
        async with message.channel.typing():
            for url in args:
                player = await YTDLSource.from_url(url, loop=self.client.loop)
                self.queues[message.guild.id].append(player)

        # start playing if not already playing
        if not vc.is_playing():
            player = self.queues[vc.guild.id][0]
            self.log_play(vc, player.title)
            vc.play(player, after=self.play_next)

        await self.send_success(message)
        await message.channel.send(Radio.queue_to_text(self.queues[message.guild.id]))

    def log_play(self, vc, title):
        username = self.client.user.name
        channel = vc.channel.name
        server = vc.guild.name
        self.lemmy.log(f'{username} 🗣️ {server}#{channel}: {title}')

    def play_next(self, error):
        # unfortunately we can't pass the voice client or other details so we have to figure out which voice client
        # needs to be started on the next track
        for vc in self.client.voice_clients:
            if not vc.is_playing():
                os.remove(self.queues[vc.guild.id][0].filename)
                del self.queues[vc.guild.id][0]

                if len(self.queues[vc.guild.id]) > 0:
                    player = self.queues[vc.guild.id][0]
                    self.log_play(vc, player.title)
                    vc.play(player, after=self.play_next)

    def queue_to_text(queue):
        if len(queue) == 0:
            return '```\nQueue is empty\n```'

        digits = len(str(len(queue)))

        tracks = []
        for i, player in enumerate(queue):
            index = i + 1
            tracks.append(f'{index:{digits}}. {player.title}')

        text = '```\n' + '\n'.join(tracks) + '\n```'

        return text

    docs_radio_queue = {
        'description': 'Displays the audio queue',
        'usage': 'radio_queue',
    }
    async def cmd_radio_queue(self, message, args, kwargs):
        if message.guild.voice_client is None:
            await self.send_error(message)
            return

        queue = self.queues[message.guild.id]

        await message.channel.send(Radio.queue_to_text(queue))

    async def on_voice_state_update(self, member, before, after):
        lemmy_voice = member.guild.voice_client
        if lemmy_voice is None:
            # Lemmy wasn't connected
            return

        if before.channel != lemmy_voice.channel:
            # Lemmy wasn't in that channel
            return

        if len(lemmy_voice.channel.members) == 1:
            # Lemmy is alone, time to leave
            self.queues[lemmy_voice.guild.id] = []
            await lemmy_voice.disconnect()

    docs_radio_off = {
        'description': 'Disconnects the radio',
        'usage': 'radio_off',
    }
    async def cmd_radio_off(self, message, args, kwargs):
        vc = message.guild.voice_client

        if vc is None:
            await self.send_error(message)
            return

        if vc.is_playing():
            vc.stop()
        await vc.disconnect()

        await self.send_success(message)

    docs_radio_pause = {
        'description': '<not implemented>',
        'usage': 'radio_',
    }
    async def cmd_radio_pause(self, message, args, kwargs):
        pass

    docs_radio_resume = {
        'description': '<not implemented>',
        'usage': 'radio_',
    }
    async def cmd_radio_resume(self, message, args, kwargs):
        pass

    docs_radio_next = {
        'description': '<not implemented>',
        'usage': 'radio_',
    }
    async def cmd_radio_next(self, message, args, kwargs):
        pass

    docs_radio_prev = {
        'description': '<not implemented>',
        'usage': 'radio_',
    }
    async def cmd_radio_prev(self, message, args, kwargs):
        pass
