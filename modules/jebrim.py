import sys
sys.path.append('..')
from module import Module

import json
import random
import re
import requests
import discord

class Jebrim(Module):
    docs = {
        'description': 'Posts random Jebrim quotes'
    }

    def get_tweets(self):
        return self.load_data('tweets', static=True, default='[]')

    docs_jebrim_add = {
        'description': 'Adds a new Jebrim screenshot to the list',
        'usage': 'jebrim_add <link>'
    }
    async def cmd_jebrim_add(self, message, args, kwargs):
        if len(args) != 1:
            await self.send_error(message)
            return

        if not re.match('https://cdn\.discordapp\.com/attachments/[0-9]+/[0-9]+/.+\.(png|jpg)/?', args[0]):
            await self.send_error(message, comment='link must be a Discord direct link')
            return

        tweets = self.get_tweets()

        if args[0] in tweets:
            await self.send_error(message, comment='link already exists in database')
            return

        tweets.append(args[0])
        self.save_data('tweets', tweets, static=True)
        await self.send_success(message)

    docs_jebrim = {
        'description': 'Posts a random Jebrim quote'
    }
    async def cmd_jebrim(self, message, args, kwargs):
        tweets = self.get_tweets()

        if len(tweets) == 0:
            await self.send_error(message, 'Jebrim database is empty')
        else:
            await message.channel.send(random.choice(tweets))

    docs_jebrim_dump = {
        'description': 'Sends a file containing the entire Jebrim database'
    }
    async def cmd_jebrim_dump(self, message, args, kwargs):
        await self.lemmy.send_text_file('\n'.join(self.get_tweets()), message.channel, file_name='jebrim-tweets.txt')
