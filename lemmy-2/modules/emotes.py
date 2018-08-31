import sys
sys.path.append('..')
from module import Module

import discord
import os
import io

WEBHOOK_NAME = 'Lemmy Emotes'
EMOTE_PATH = '../pics/emotes'

# TODO: extract static to config level

class Emotes(Module):
    docs = {
        'description': 'Handles emotes and stickers'
    }

    def __init__(self, client):
        Module.__init__(self, client)

        self.load_all()


    def _load_images(self, type):
        files = self.list_files(type, static=True)
        images = filter(lambda file_name: file_name.endswith('.gif') or file_name.endswith('.png'), files)
        trimmed_images = map(lambda file_name: '.'.join(file_name.split('.')[:-1]), images)
        return set(trimmed_images)

    def load_emotes(self):
        self.emotes = self._load_images('emote')

    def load_stickers(self):
        self.stickers = self._load_images('sticker')

    def load_all(self):
        self.load_emotes()
        self.load_stickers()

    def _get_image_filename(self, type, emote_name):
        if self.data_exists(f'{type}/{emote_name}.gif', static=True):
            return f'{emote_name}.gif'
        elif self.data_exists(f'{type}/{emote_name}.png', static=True):
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

    # async def on_message(self, message):
    #     if message.content in self.media:
    #         webhook = await self.get_webhook(message.channel)

    #         with open(f'{EMOTE_PATH}/{imagePath}', 'rb') as image:
    #             file = discord.File(fp=image, filename=self.media[message.content])
    #             await webhook.send(username=message.author.display_name, avatar_url=message.author.avatar_url, file=file)
    #             await message.delete()

    async def send_image(self, name, destination, type, vanity_username=None, vanity_avatar_url=None):
        image_file_name = self.get_image_filename(name)
        image_file = self.get_image_as_discord_file(image_file_name, type)
        webhook = await self.get_webhook(destination, WEBHOOK_NAME)

        await webhook.send(username=vanity_username,
                            avatar_url=vanity_avatar_url,
                            file=image_file)

    async def cmd_send_image(self, message, args, kwargs):
        await self.send_image(args[0], message.channel, 'emote', vanity_username=message.author.name, vanity_avatar_url=message.author.avatar_url)
        await message.delete()

    async def cmd_emote_list(self, message, args, kwargs):
        await message.channel.send(self.emotes)

    async def cmd_sticker_list(self, message, args, kwargs):
        await message.channel.send(self.stickers)
