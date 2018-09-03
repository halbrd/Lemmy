import sys
sys.path.append('..')
from module import Module

import discord
import os
import io

WEBHOOK_NAME = 'Lemmy Emotes'
EMOTE_MAX_SIZE = 64, 64
STICKER_MAX_SIZE = 128, 128

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

        args = Module.deconstruct_message(message)['args']

        delete_message = False
        for arg in args:
            discord_file = None

            if arg in self.emotes:
                discord_file = self.get_image_as_discord_file(self.emotes[arg], 'emote')
            elif arg in self.stickers:
                discord_file = self.get_image_as_discord_file(self.stickers[arg], 'sticker')

            if discord_file:
                await self.send_image(discord_file, message.channel, vanity_username=message.author.name,
                vanity_avatar_url=message.author.avatar_url)
                delete_message = True

        if delete_message:
            await message.delete()

    def _load_emoters(self, emoter_type):
        # list all files in emoter directory
        files = self.list_files(emoter_type, static=True)

        # filter out files that can't be an emoter
        is_valid_emoter = lambda file_name: file_name.endswith('.gif') or file_name.endswith('.png')
        emoter_files = filter(is_valid_emoter, files)

        # map emoter names to emoter file names
        return {
            '.'.join(emoter_file.split('.')[:-1]): emoter_file
            for emoter_file in emoter_files
        }

    def load_emotes(self):
        self.emotes = self._load_emoters('emote')

    def load_stickers(self):
        self.stickers = self._load_emoters('sticker')

    # TODO: refactor into filename -> bytes, bytes -> discordfile
    def get_image_as_discord_file(self, file_name, emoter_type):
        image_bytes = self.load_image(f'{emoter_type}/{file_name}', static=True)
        image_file = io.BytesIO(image_bytes)
        discord_file = discord.File(fp=image_file, filename=file_name)
        return discord_file

    async def get_webhook(self, channel, webhook_name):
        return discord.utils.find(lambda x: x.name == webhook_name, await channel.webhooks()) or await channel.create_webhook(name=webhook_name)

    async def send_image(self, discord_file, destination, vanity_username=None, vanity_avatar_url=None):
        webhook = await self.get_webhook(destination, WEBHOOK_NAME)
        await webhook.send(username=vanity_username, avatar_url=vanity_avatar_url, file=discord_file)

    async def cmd_emoter_list(self, message, args, kwargs):
        await message.channel.send('Emotes: ' + str(self.emotes))
        await message.channel.send('Stickers: ' + str(self.stickers))

    def normalize_png(self, png_bytes, target_size):
        # load bytes into PIL Image
        image_file = io.BytesIO(png_bytes)
        im = Image.open(image_file)

        # resize image, maintaining aspect ratio
        im.thumbnail(target_size, Image.ANTIALIAS)

        # pad image out to a square
        horizontal_padding = target_size[0] - image.size[0]
        vertical_padding = target_size[1] - image.size[1]

        square_image = Image.new(im.mode, target_size)
        square_image.putalpha(0)   # fill image with transparent
        square_image.paste(im, (horizontal_padding // 2, vertical_padding // 2))   # paste emote in center
        image = square_image

        # return bytes
        output_file = io.BytesIO()
        im.save(output_file, 'PNG')
        return output_file.getvalue()
