import sys
sys.path.append('..')
from module import Module

import requests
import pathlib
import discord
import os

CACHE_LOC = pathlib.Path('cache/Imgur/')

class Imgur(Module):
    docs = {
        'description': 'Tools for getting off imgur'
    }

    docs_imgur_rehost = {
        'description': 'Uploads imgur links to Discord and gives you the new links'
    }
    async def cmd_imgur_rehost(self, message, args, kwargs):
        text_files = [ file for file in message.attachments if file.filename.endswith('.txt') ]

        for file in text_files:
            contents = (await file.read()).decode()
            args += contents.strip().split('\n')

        results = []
        files = []

        for arg in args:
            if not 'i.imgur.com' in arg:
                results.append(f'{arg}: not an i.imgur.com link')
                continue

            r = requests.get(arg, stream=True)

            if r.status_code != 200:
                results.append(f'{arg}: HTTP {r.status_code}')
                continue

            slug = arg.split('/')[-1].split('.')[0]
            ext = arg.split('/')[-1].split('.')[1]
            file = f'{slug}.{ext}'

            if not CACHE_LOC.exists():
                CACHE_LOC.mkdir(parents=True, exist_ok=True)

            cache_dest = CACHE_LOC / file
            with open(cache_dest, 'wb') as f:
                for chunk in r:
                    f.write(chunk)

            with open(cache_dest, 'rb') as f:
                image = discord.File(f, filename='imgur_' + file)
                message = await message.channel.send(file=image)

            results.append(message.attachments[0].url)

            os.remove(cache_dest)

        await self.lemmy.send_text_file('\n'.join(results), message.channel, file_name='discord-links.txt')
