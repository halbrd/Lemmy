import sys
sys.path.append('..')
from module import Module

# I tried for a long time to call yt-dlp properly, like in Radio, but it sometimes gives HEVC (x265) (which Discord
# won't embed), and I could not for the life of me get it to use h264, or anything else, through code.

# The required CLI switch is `-S vcodec:h264`, which works fine in terminal. However I absolutely could not get it to
# work through the ytdl_opts method.

import discord
import subprocess
import os
import re

CACHE_LOC = 'cache/VideoFetch/'
ATTEMPTS = 3

def clean_filename(filename):
    for c in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
        filename = filename.replace(c, '')
    return filename

async def send_tiktok(url, channel):
    filename = CACHE_LOC + clean_filename(url) + '.mp4'

    success = False
    for i in range(ATTEMPTS):
        r = subprocess.run(['yt-dlp', '-S', 'vcodec:h264', '-o', filename, url])
        if r.returncode == 0:
            success = True
            break

    if not success:
        return

    with open(filename, 'rb') as f:
      await channel.send(file=discord.File(f))

    os.remove(filename)


class VideoFetch(Module):
    docs = {
        'description': 'Fetches videos for easier viewing'
    }

    async def on_message(self, message):
        if message.author == self.client.user:
            # just in case
            return

        for match in re.findall('https?://vt.tiktok.com/[A-Za-z0-9]+', message.content):
            await send_tiktok(match, message.channel)
