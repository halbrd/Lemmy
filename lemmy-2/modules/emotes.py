import sys
sys.path.append('..')
from module import Module

import discord
import os
import io

WEBHOOK_NAME = 'Lemmy Emotes'
USE_STATIC_STORAGE = True   # this might be better as a member variable so it can be changed at runtime

class Emotes(Module):
    docs = {
        'description': 'Handles emotes and stickers'
    }

    def __init__(self, client):
        Module.__init__(self, client)

        self.load_emotes()
        self.load_stickers()

    async def on_message(self, message):
        if message.content in self.emotes:
            await self.send_image(message.content, 'emote', message.channel,
              vanity_username=message.author.name, vanity_avatar_url=message.author.avatar_url)

        if message.content in self.stickers:
            await self.send_image(message.content, 'sticker', message.channel,
              vanity_username=message.author.name, vanity_avatar_url=message.author.avatar_url)

        if message.content in self.emotes or message.content in self.stickers:
            await message.delete()

    def _load_images(self, type):
        files = self.list_files(type, static=USE_STATIC_STORAGE)
        images = filter(lambda file_name: file_name.endswith('.gif') or file_name.endswith('.png'), files)
        trimmed_images = map(lambda file_name: '.'.join(file_name.split('.')[:-1]), images)
        return set(trimmed_images)

    def load_emotes(self):
        self.emotes = self._load_images('emote')

    def load_stickers(self):
        self.stickers = self._load_images('sticker')

    def _get_image_filename(self, type, emote_name):
        if self.data_exists(f'{type}/{emote_name}.gif', static=USE_STATIC_STORAGE):
            return f'{emote_name}.gif'
        elif self.data_exists(f'{type}/{emote_name}.png', static=USE_STATIC_STORAGE):
            return f'{emote_name}.png'
        return None

    def get_image_filename(self, name):
        return self._get_image_filename('emote', name) or self._get_image_filename('sticker', name)

    def get_image_as_discord_file(self, file_name, type):
        image_bytes = self.load_image(type, file_name)
        image_file = io.BytesIO(image_bytes)
        discord_file = discord.File(fp=image_file, filename=file_name)
        return discord_file

    async def get_webhook(self, channel, webhook_name):
        return discord.utils.find(lambda x: x.name == webhook_name, await channel.webhooks()) or await channel.create_webhook(name=webhook_name)

    async def send_image(self, name, type, destination, vanity_username=None, vanity_avatar_url=None):
        image_file_name = self.get_image_filename(name)
        image_file = self.get_image_as_discord_file(image_file_name, type)
        webhook = await self.get_webhook(destination, WEBHOOK_NAME)

        await webhook.send(username=vanity_username,
                            avatar_url=vanity_avatar_url,
                            file=image_file)

    async def cmd_emote_list(self, message, args, kwargs):
        await message.channel.send(self.emotes)

    async def cmd_sticker_list(self, message, args, kwargs):
        await message.channel.send(self.stickers)
