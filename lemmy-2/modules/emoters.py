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

    # def normalize_png(self, png_bytes):
    #     output_size = 64, 64
        
    #     # load image
    #     image_file = io.BytesIO(png_bytes)
    #     image = Image.open(image_file)
        
    #     # resize
    #     image.thumbnail(output_size, Image.ANTIALIAS)

    #     # pad
    #     horizontal_padding = output_size[0] - image.size[0]
    #     vertical_padding = output_size[1] - image.size[1]

    #     # center image
    #     square_image = Image.new(image.mode, output_size)
    #     square_image.putalpha(0)
    #     square_image.paste(image, (horizontal_padding // 2, vertical_padding // 2))
    #     image = square_image

    #     # return bytes
    #     output_file = io.BytesIO()
    #     image.save(output_file, 'PNG')

    #     return output_file.getvalue()

    # def normalize_gif(self, gif_bytes, channel):
    #     output_size = 32, 32

    #     # load image
    #     image_file = io.BytesIO(gif_bytes)
    #     image = Image.open(image_file)
    #     frames = list(ImageSequence.Iterator(image))
        
    #     for i, frame in enumerate(frames):
    #         frame.thumbnail(output_size, Image.ANTIALIAS)

    #         # pixels = frame.load()

    #         # for y in range(frame.size[1]):
    #         #     for x in range(frame.size[0]):
    #         #         # if pixels[x, y] == 6:
    #         #         #     pixels[x, y] = 0
    #         #         print(pixels[x, y], end='|')

    #         # frame.save(f'frame{i}.gif')
    #         # break



    #     #     # resize
    #     #     frames[i].thumbnail(output_size, Image.ANTIALIAS)

    #     #     # pad
    #     #     horizontal_padding = output_size[0] - frame.size[0]
    #     #     vertical_padding = output_size[1] - frame.size[1]

    #     #     # center image
    #     #     square_image = Image.new(frame.mode, output_size)
    #     #     square_image.putalpha(0)
    #     #     square_image.paste(frame, (horizontal_padding // 2, vertical_padding // 2))
    #     #     square_image = square_image.rotate(90)
    #     #     frames[i] = square_image
        
    #     # return bytes
    #     output_file = io.BytesIO()
    #     initial_frame = frames[0]
    #     initial_frame.save(output_file, 'GIF', save_all=True, append_images=list(frames[1:]))

    #     return output_file.getvalue()

