import sys
sys.path.append('..')
from module import Module

import discord
import os
import io

WEBHOOK_NAME = 'Lemmy Emotes'
EMOTE_PATH = '../pics/emotes'

class Emotes(Module):
    docs = {
        'description': 'Handles emotes'
    }

    def __init__(self, client):
        Module.__init__(self, client)

        self.media = {}
        for f in (f for f in os.listdir(EMOTE_PATH) if os.path.isfile(os.path.join(EMOTE_PATH, f))):
            emote, ext = f.split('.')
            self.media[emote] = f

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
        image_data = self.load_image(type, name)
        webhook = await self.get_webhook(destination, WEBHOOK_NAME)

        image_file = io.BytesIO(image_data['bytes'])
        discord_file = discord.File(fp=image_file, filename=f'{name}.{image_data["extension"]}')

        await webhook.send(username=vanity_username,
                            avatar_url=vanity_avatar_url,
                            file=discord_file)

    async def cmd_send_image(self, message, args, kwargs):
        await self.send_image(args[0], message.channel, 'emote', vanity_username=message.author.name, vanity_avatar_url=message.author.avatar_url)
        await message.delete()
