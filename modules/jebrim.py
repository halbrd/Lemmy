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

        if not re.match('https://i\.imgur\.com/[A-Za-z0-9]+\.(png|jpg)/?', args[0]):
            await self.send_error(message, comment='link must be an Imgur direct link')
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

    docs_is_jebrim_suspended = {
        'description': 'Checks if Jebrim is suspended on Twitter'
    }
    async def cmd_is_jebrim_suspended(self, message, args, kwargs):
        accounts = ['Jebrim', 'The1Jebrim', 'mirbeJ', 'FakeJebrim', 'Agilitism']
        account_lines = []

        for account in accounts:
            suspended = 'This account has been suspended' in requests.get('https://twitter.com/' + account).text
            indicator = '💔' if suspended else '💚'
            line = f'{indicator} [@{account}](https://twitter.com/{account})'
            account_lines.append(line)

        embed = discord.Embed()
        embed.description = '\n'.join(account_lines)
        await message.channel.send(embed=embed)

    docs_jebrim_dump = {
        'description': 'Sends a file containing the entire Jebrim database'
    }
    async def cmd_jebrim_dump(self, message, args, kwargs):
        await self.lemmy.send_text_file('\n'.join(self.get_tweets()), message.channel, file_name='jebrim-tweets.txt')
