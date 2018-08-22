import sys
sys.path.append('..')
from module import Module

import discord

WEBHOOK_NAME = 'WEBHOOK_BOT'
EMOTE_PATH = '../pics/emotes'

class Emotes(Module):
    docs = {
        'description': 'Handles emotes'
    }

    def __init__(self, client):
        self.media = {}
        for f in (f for f in os.listdir(EMOTE_PATH) if os.path.isfile(os.path.join(EMOTE_PATH, f))):
            emote, ext = f.split('.')
            self.media[emote] = f

    async def get_webhook(self, channel):
        if not WEBHOOK_NAME in await channel.webhooks():
            await channel.create_webhook(name=WEBHOOK_NAME)

        return await channel.webhooks()[WEBHOOK_NAME]

    async def on_message(self, message):
        if message.content in self.media:
            webhook = await self.get_webhook(message.channel)

            with open(f'{EMOTE_PATH}/{imagePath}', 'rb') as image:
                file = discord.File(fp=image, filename=self.media[message.content])
                await webhook.send(username=message.author.display_name, avatar_url=message.author.avatar_url, file=file)
                await message.delete()
