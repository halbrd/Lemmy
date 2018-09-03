import sys
sys.path.append('..')
from module import Module

import discord
import os
import io

WEBHOOK_NAME = 'Lemmy Emotes'

class Emoters(Module):
    docs = {
        'description': 'Handles emotes and stickers'
    }

    def __init__(self, client):
        Module.__init__(self, client)

        self.load_emotes()
        self.load_stickers()

    async def on_message(self, message):
        await self.call_functions(message)

        if message.content.startswith('^'):
            message.content = message.content[1:]

        discord_file = None

        if message.content in self.instantial_emotes:
            discord_file = self.get_image_as_discord_file(self.instantial_emotes[message.content], 'emote', static=False)

        elif message.content in self.static_emotes:
            discord_file = self.get_image_as_discord_file(self.static_emotes[message.content], 'emote', static=True)

        elif message.content in self.instantial_stickers:
            discord_file = self.get_image_as_discord_file(self.instantial_stickers[message.content], 'sticker', static=False)

        elif message.content in self.static_stickers:
            discord_file = self.get_image_as_discord_file(self.static_stickers[message.content], 'sticker', static=True)

        if discord_file:
            await self.send_image(discord_file, message.channel, vanity_username=message.author.name,
              vanity_avatar_url=message.author.avatar_url)
            await message.delete()

    def _load_emoters(self, emoter_type, static):
        # list all files in emoter directory
        files = self.list_files(emoter_type, static=static)

        # filter out files that can't be an emoter
        is_valid_emoter = lambda file_name: file_name.endswith('.gif') or file_name.endswith('.png')
        emoter_files = filter(is_valid_emoter, files)

        # map emoter names to emoter file names
        return {
            '.'.join(emoter_file.split('.')[:-1]): emoter_file
            for emoter_file in emoter_files
        }

    def load_emotes(self):
        self.static_emotes = self._load_emoters('emote', static=True)
        self.instantial_emotes = self._load_emoters('emote', static=False)

    def load_stickers(self):
        self.static_stickers = self._load_emoters('sticker', static=True)
        self.instantial_stickers = self._load_emoters('sticker', static=False)

    def get_image_as_discord_file(self, file_name, emoter_type, static):
        image_bytes = self.load_image(f'{emoter_type}/{file_name}', static=static)
        image_file = io.BytesIO(image_bytes)
        discord_file = discord.File(fp=image_file, filename=file_name)
        return discord_file

    async def get_webhook(self, channel, webhook_name):
        return discord.utils.find(lambda x: x.name == webhook_name, await channel.webhooks()) or await channel.create_webhook(name=webhook_name)

    async def send_image(self, discord_file, destination, vanity_username=None, vanity_avatar_url=None):
        webhook = await self.get_webhook(destination, WEBHOOK_NAME)

        await webhook.send(username=vanity_username,
                            avatar_url=vanity_avatar_url,
                            file=discord_file)

    async def cmd_emoter_list(self, message, args, kwargs):
        await message.channel.send('Static emotes: ' + str(self.static_emotes))
        await message.channel.send('Instantial emotes: ' + str(self.instantial_emotes))
        await message.channel.send('Static stickers: ' + str(self.static_stickers))
        await message.channel.send('Instantial stickers: ' + str(self.instantial_stickers))
