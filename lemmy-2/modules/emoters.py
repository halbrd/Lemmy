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

# TODO: delete code
# TODO: user-facing documentation
# TODO: make relevant functions static
# TODO: scale modifiers

class Emoters(Module):
    docs = {
        'description': 'Handles emotes and stickers'
    }

    MODIFIERS = {
        'rotate': {
            'validate': lambda x: bool(re.fullmatch('-?\d+', x)),
            'transform': lambda x: int(x),
            'apply': lambda image, x: image.rotate(x)
        },
        'flip': {
            'validate': lambda x: bool(re.fullmatch('[vh]', x)),
            'transform': lambda x: x,
            'apply': lambda image, x: image.flip() if x == 'v' else image.flop()
        }
    }

    def __init__(self, client):
        Module.__init__(self, client)

        self.load_emotes()
        self.load_stickers()

    async def on_message(self, message):
        await self.call_functions(message)

        # transform message into arguments, and pre-emptively split emoter name and rules
        # e.g. DOSCassidy/rotate:45/flip:h
        #   -> ['DOSCassidy', 'rotate:45', 'flip:h']
        args = Module.deconstruct_message(message)['args']
        args = [ arg.split(OPERATION_DELIMITER) for arg in args ]

        # check if every arg is a valid emote, and stop here if this is not the case
        everything_is_an_emoter = len(args) > 0 and all([self.is_emoter(arg[0]) for arg in args])
        if not everything_is_an_emoter:
            return

        # transform emoter name and modifiers into a dictionary
        # example:
        # {
        #   'name': 'DOSCassidy',
        #   'type': 'emote',
        #   'static': True,
        #   'modifications': [ ('rotate', 45), ('flip', 'h') ]
        # }
        emoters = []
        for emoter_phrase in args:
            # initialise emoter_details with attributes: name, type, static
            emoter_details = self.get_emoter_details_by_name(emoter_phrase[0])
            # add in emoter name
            emoter_details['name'] = emoter_phrase[0]
            # add in modifications
            try:
                emoter_details['modifications'] = Emoters._split_raw_modifiers(emoter_phrase[1:])
            except ValueError:
                await self.send_error(message)
                return

            emoters.append(emoter_details)

        # transform emoter details into list of processed (with modifiers applied) Wand images
        images = []
        for emoter in emoters:
            image_bytes = self.get_image_bytes(emoter['file_name'], emoter['type'], emoter['static'])

            images.append(Emoters.process_image(image_bytes, emoter['modifications']))

        # assemble all images into single image to send
        if len(images) == 1:   # skip compositing if there's only 1 image, mainly to allow GIFs to remain animated
            base_image = images[0]
        else:
            base_image = Image(width=sum(image.size[0] for image in images), height=max(image.size[1] for image in images))
            base_image.format = 'png'
            x_cursor = 0

            for image in images:
                base_image.composite(image.sequence[0], left=x_cursor, top=(base_image.size[1] - image.size[1]) // 2)
                x_cursor += image.size[0]

        # send image
        file_name = ''.join([ emoter['name'] for emoter in emoters ]) + ('.gif' if base_image.format.lower() == 'gif' else '.png')
        discord_file = self.lemmy.to_discord_file(base_image.make_blob(), file_name)
        await self.send_image(discord_file, message.channel, vanity_username=message.author.name,
            vanity_avatar_url=message.author.avatar_url)

    def _split_raw_modifiers(raw_modifiers):
        # e.g. ['rotate:45', 'flip:h']
        #   -> [ ('rotate', '45'), ('flip', 'h') ]

        modifiers = []

        for raw_modifier in raw_modifiers:
            # split the modifier string
            modifier_terms = tuple(raw_modifier.split(OPERATION_PARAM_DELIMITER))

            # check that there's exactly 1 parameter
            if len(modifier_terms) != 2:
                raise ValueError('modifiers must have exactly 1 parameter')

            # there are two modifier terms - we can assign them names for clarity
            modifier, parameter = modifier_terms

            # validate modifier name and parameter
            if not Emoters.MODIFIERS[modifier]['validate'](parameter):
                raise ValueError(f'\'{modifier}: {parameter}\' is not a valid modifier')

            # transform parameter
            parameter = Emoters.MODIFIERS[modifier]['transform'](parameter)

            # add our processed modifier to the list
            modifiers.append((modifier, parameter))

        return modifiers


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
        return name in self.static_emotes \
          or name in self.static_stickers \
          or name in self.instance_emotes \
          or name in self.instance_stickers

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

    def _scale_frame(frame, side_length, preserve_aspect_ratio):
        if preserve_aspect_ratio:
            frame.transform(resize=f'{side_length}x{side_length}')
        else:
            frame.resize(side_length, side_length)
        return frame

    def scale_image(image, side_length, preserve_aspect_ratio=True):
        """ Scales a Wand image such that its longest side equals side_length """
        new_image = Image()

        for frame in image.sequence:
            new_image.sequence.append(Emoters._scale_frame(frame, side_length, preserve_aspect_ratio))

        return new_image

    def _pad_frame(frame):
        # get a new empty SingleImage of the desired size
        new_frame = frame.clone()
        new_frame.transparentize(transparency=1)
        target_side_length = max(frame.size)
        new_frame.resize(width=target_side_length, height=target_side_length)

        # paste the frame in the middle
        pad_left = (target_side_length - frame.size[0]) // 2
        pad_top = (target_side_length - frame.size[1]) // 2
        new_frame.composite(frame, left=pad_left, top=pad_top)

        return new_frame

    def pad_image(image):
        """ Pads a Wand image with transparency such that its shortest side becomes equal to its longest side """
        new_image = Image()

        for frame in image.sequence:
            new_image.sequence.append(Emoters._pad_frame(frame))

        return new_image

    def normalize_image(image, side_length=None, pad=True):
        if side_length:
            image = Emoters.scale_image(image, side_length)

        if pad:
            image = Emoters.pad_image(image)

        return image

    def process_image(image_bytes, modifications):
        # turn image bytes into Wand image
        image = Image(blob=image_bytes)

        # normalize image (scale to correct size, pad with transparency to make square)
        image = Emoters.normalize_image(image, side_length=EMOTE_MAX_SIZE, pad=True)

        # apply modifiers
        for modifier, parameter in modifications:
            Emoters.MODIFIERS[modifier]['apply'](image, parameter)

        return image

    async def cmd_emoter_search(self, message, args, kwargs):
        pass   # TODO


#################
### TO DELETE ###
#################


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


    async def cmd_emoter_list(self, message, args, kwargs):
        await message.channel.send('Static emotes: ' + str(self.static_emotes))
        await message.channel.send('Instance emotes: ' + str(self.instance_emotes))
        await message.channel.send('Static stickers: ' + str(self.static_stickers))
        await message.channel.send('Instance stickers: ' + str(self.instance_stickers))

    async def cmd_test_wand(self, message, args, kwargs):
        img_bytes = self.get_image_bytes('Konga.gif', 'emote', True)
        image = Image(blob=img_bytes)
        await message.channel.send(f'frames: {len(image.sequence)}')

        image = self.normalize_image(image, EMOTE_MAX_SIZE)

        img_bytes = image.make_blob()
        discord_file = self.lemmy.to_discord_file(img_bytes, 'Konga.gif')
        await self.send_image(discord_file, message.channel, vanity_username=message.author.name,
          vanity_avatar_url=message.author.avatar_url)

    async def cmd_frame_dimensions(self, message, args, kwargs):
        deets = self.get_emoter_details_by_name(args[0])
        img_bytes = self.get_image_bytes(deets['file_name'], deets['type'], deets['static'])
        image = Image(blob=img_bytes)
        print(f'{type(image)}: {image.size}')
        for frame in image.sequence:
            print(f'{type(frame)}: {frame.size}')


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
