import sys
sys.path.append('..')
from module import Module

import re
import random

class Neet(Module):
    docs = {
        'description': 'Censors the word \'neet\''
    }

    def __init__(self, lemmy):
        Module.__init__(self, lemmy)

        self.words = self.load_data('words', static=True, default=[])

    def replace_neet(self, input):
        caps_indices = [i for i, char in enumerate(input.group()) if char.isupper()]
        replacement = list(random.choice(self.words))
        for i in caps_indices:
            replacement[i] = replacement[i].upper()
        return ''.join(replacement)

    async def on_message(self, message):
        await self.call_functions(message)

        if not 'wish i was neet' in message.content.lower():
            return

        body = re.sub(
            'neet',
            self.replace_neet,
            message.content,
            flags=re.IGNORECASE
        )

        webhook = await self.lemmy.get_webhook(message.channel)
        await webhook.send(
            body,
            username=message.author.display_name,
            avatar_url=message.author.display_avatar.url
        )
        await message.delete()
