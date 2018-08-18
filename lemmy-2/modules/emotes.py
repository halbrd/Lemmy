import sys
sys.path.append('..')
from module import Module

from discord import File
from os import listdir
from os.path import isfile, join

WEBHOOK_NAME = 'WEBHOOK_BOT'
EMOTE_PATH = '../pics/emotes'

class Emotes(Module):
    docs = {
            'description': 'Handles emotes'
            }

    def __init__(self, client):
        self.media = {}
        for f in (f for f in listdir(EMOTE_PATH) if isfile(join(EMOTE_PATH, f))):
            emote, ext = f.split('.')
            self.media[emote] = f

    async def get_or_create_webhook(self, channel):
        webhooks = await channel.webhooks()
        if WEBHOOK_NAME in webhooks:
            return webhooks[WEBHOOK_NAME]
        else:
            webhook = await channel.create_webhook(name=WEBHOOK_NAME)
            return webhook

    async def on_message(self, message):
        if message.content in self.media:
            webhook = await self.get_or_create_webhook(message.channel)

            display_name = message.author.display_name
            avatar_url = message.author.avatar_url
            imagePath = self.media[message.content]

            with open(f'{EMOTE_PATH}/{imagePath}', 'rb') as image:
                file = File(fp=image, filename=imagePath)
                await webhook.send(username=display_name, avatar_url=avatar_url, file=file)
                await message.delete()
