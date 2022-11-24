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

DOWNLOAD_PATTERNS = [
    re.compile('https?://\w+.tiktok.com/[^ ]+'),

    re.compile('https?://\w+.reddit.com/r/\w+/comments/\w+.*'),
    re.compile('https?://v.redd.it/\w+'),
    re.compile('https?://redd.it/\w+'),
]

def clean_filename(filename):
    for c in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
        filename = filename.replace(c, '')
    return filename

async def download_and_send(url, channel):
    base_filename = clean_filename(url)
    base_file_loc = CACHE_LOC + base_filename

    expected_filename = base_filename + '.mp4'
    expected_file_loc = CACHE_LOC + base_filename + '.mp4'

    success = False
    for i in range(ATTEMPTS):
        r = subprocess.run(['yt-dlp', '-S', 'vcodec:h264', '-o', base_file_loc + '.%(ext)s', url])
        if r.returncode == 0:
            success = True
            break

    if not success:
        return

    matching_files = [
        f for f in os.listdir(CACHE_LOC)
        if f.startswith(base_filename)
    ]

    if expected_filename in matching_files:
        try:
            with open(expected_file_loc, 'rb') as f:
                await channel.send(file=discord.File(f))
        except:
            pass

    for f in matching_files:
        os.remove(CACHE_LOC + f)


class VideoFetch(Module):
    docs = {
        'description': 'Fetches videos for easier viewing'
    }

    async def on_message(self, message):
        if message.author == self.client.user:
            # just in case
            return

        for pattern in DOWNLOAD_PATTERNS:
            for match in re.findall(pattern, message.content):
                await download_and_send(match, message.channel)
