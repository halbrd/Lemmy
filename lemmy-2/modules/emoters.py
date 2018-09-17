import sys
sys.path.append('..')
from module import Module

import discord
import os
import io
from wand.image import Image, Color
import re

WEBHOOK_NAME = 'Lemmy Emotes'
EMOTE_MAX_SIZE = 64
STICKER_MAX_SIZE = 128
OPERATION_DELIMITER = '/'
OPERATION_PARAM_DELIMITER = ':'

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
        args = list(map(lambda arg: arg.split(OPERATION_DELIMITER), args))

        if len(args) > 0 and all([self.is_emoter(arg[0]) for arg in args]):   # every arg is a valid emote
            # collect details and parse operations into convenient dictionary
            emoters = []
            for emoter_phrase in args:
                emoter = self.get_emoter_details_by_name(emoter_phrase[0])
                emoter['name'] = emoter_phrase[0]
                emoter['steps'] = []

                for step in emoter_phrase[1:]:
                    assert len(step.split(OPERATION_PARAM_DELIMITER)) == 2
                    emoter['steps'].append((step.split(OPERATION_PARAM_DELIMITER)[0], step.split(OPERATION_PARAM_DELIMITER)[1]))

                emoters.append(emoter)

            # assemble list of processed emotes as Wand images
            images = []
            for emoter in emoters:
                # validate suffixes
                # skipping for now to reduce complexity in development

                image_bytes = self.get_image_bytes(emoter['file_name'], emoter['type'], emoter['static'])

                images.append(self.process_image(image_bytes, emoter['steps']))

            if len(images) == 1:   # skip compositing if there's only 1 image, mainly to allow GIFs to remain animated
                base_image = images[0]
            else:
                base_image = Image(width=sum(image.size[0] for image in images), height=max(image.size[1] for image in images))
                base_image.format = images[0].format.lower()
                x_cursor = 0

                for image in images:
                    base_image.composite(image, left=x_cursor, top=(base_image.size[1] - image.size[1]) // 2)
                    x_cursor += image.size[0]

            discord_file = self.lemmy.to_discord_file(base_image.make_blob(), emoter['file_name'])
            await self.send_image(discord_file, message.channel, vanity_username=message.author.name,
              vanity_avatar_url=message.author.avatar_url)

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
        self.instance_emotes = self._load_emoters('emote', static=False)

    def load_stickers(self):
        self.static_stickers = self._load_emoters('sticker', static=True)
        self.instance_stickers = self._load_emoters('sticker', static=False)

    def get_image_bytes(self, file_name, emoter_type, static):
        return self.load_image(f'{emoter_type}/{file_name}', static=static)

    def is_emoter(self, name):
        return name in self.static_emotes or name in self.static_stickers or name in self.instance_emotes or name in self.instance_stickers

    def get_emoter_details_by_name(self, name):
        emoter_details = None

        if name in self.instance_emotes:
            emoter_details = (self.instance_emotes[name], 'emote', False)
        elif name in self.instance_stickers:
            emoter_details = (self.instance_stickers[name], 'sticker', False)
        elif name in self.static_emotes:
            emoter_details = (self.static_emotes[name], 'emote', True)
        elif name in self.static_stickers:
            emoter_details = (self.static_stickers[name], 'sticker', True)

        if emoter_details is None:
            return None
        else:
            return {
                'file_name': emoter_details[0],
                'type': emoter_details[1],
                'static': emoter_details[2]
            }

    async def get_webhook(self, channel, webhook_name):
        return discord.utils.find(lambda x: x.name == webhook_name, await channel.webhooks()) or await channel.create_webhook(name=webhook_name)

    async def send_image(self, discord_file, destination, vanity_username=None, vanity_avatar_url=None):
        webhook = await self.get_webhook(destination, WEBHOOK_NAME)
        await webhook.send(username=vanity_username, avatar_url=vanity_avatar_url, file=discord_file)

    async def cmd_emoter_list(self, message, args, kwargs):
        await message.channel.send('Static emotes: ' + str(self.static_emotes))
        await message.channel.send('Instance emotes: ' + str(self.instance_emotes))
        await message.channel.send('Static stickers: ' + str(self.static_stickers))
        await message.channel.send('Instance stickers: ' + str(self.instance_stickers))

    def normalize_png_pillow(self, png_bytes, target_size):
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

    def normalize_image(self, image_seq, side_length=None, pad=True):
        for i, image in enumerate(image_seq.sequence):
            # resize image, maintaining aspect ratio
            if side_length:
                image.transform(resize=f'x{side_length}')

            # pad image with transparency so that it's square
            if pad:
                target_side_length = max(image.size)
                pad_left = target_side_length - image.size[0]
                pad_top = target_side_length - image.size[1]

                new_image = Image(width=target_side_length, height=target_side_length, background=Color('transparent'))
                new_image.format = image_seq.format.lower()
                new_image.composite(image, left=pad_left // 2, top=pad_top // 2)
                image = new_image

            image_seq.sequence[i] = image

        return image_seq

    def process_image(self, image_bytes, steps):
        image = Image(blob=image_bytes)

        image = self.normalize_image(image, EMOTE_MAX_SIZE)

        for step in steps:

            if step[0] == 'flip':
                if step[1] == 'v':
                    image.flip()
                elif step[1] == 'h':
                    image.flop()
                else:
                    raise ValueError("image flip parameter must be 'v' or 'h'")

            elif step[0] == 'rotate':
                image.rotate(int(step[1]))

            else:
                raise ValueError(f"'{step[0]}' is not a valid image operation")

        return image

    async def cmd_test_wand(self, message, args, kwargs):
        img_bytes = self.get_image_bytes('Konga.gif', 'emote', True)
        image = Image(blob=img_bytes)
        await message.channel.send(f'frames: {len(image.sequence)}')

        image = self.normalize_image(image, EMOTE_MAX_SIZE)

        img_bytes = image.make_blob()
        discord_file = self.lemmy.to_discord_file(img_bytes, 'Konga.gif')
        await self.send_image(discord_file, message.channel, vanity_username=message.author.name,
          vanity_avatar_url=message.author.avatar_url)


### Much Ado About Images ###
# Problem: PIL can't render gifs with transparency
# Issues this causes:
# - Can't automatically resize gifs
# - Can't combine gifs with other images
# Potential solutions:
# - Drop PIL for ImageMagick
#   Advantages:
#   - Actually solves the problem
#   Disadvantages:
#   - Creates platform dependency, increasing deployment complexity, probably necessitating Docker
#   - Not certain that ImageMagick will have all benefits of PIL, eg. in-memory handling, padding
# - Don't support gif manipulation
#   Advantages:
#   - Low complexity, little effort
#   Disadvantages:
#   - Increases user effort and proficiency requirement
#   - Lack of features

# ImageMagick capabilities
# Can do:
# - Rotate, resize PNGs, maintain transparency, aspect ratio
#   `convert -background transparent -rotate 30 -resize 64x64 in.png out.png`
# - Rotate, resize GIFs, maintain transparency, aspect ratio (places image frame-by-frame?????)
#   `convert -background none -rotate 30 -resize 64x64 in.gif out.gif`
# - Connect PNGs horizontally, auto spaced and laid out
#   `montage -background transparent -geometry +0+0 in1.png in2.png out.png`
# - Connect PNGs and the first frame of a gif
#   `montage -background transparent -geometry +0+0 in1.png 'in2.gif[0]' out.png`
# - Rotate or flip images, then connect
#   ``
# Okay you know what I'm pretty sure it can do everything needed
# Can't do:
