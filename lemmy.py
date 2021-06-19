import discord
import datetime
import asyncio
import os
import os.path
import json
import importlib
import sys
import re
from itertools import zip_longest
import logging
import signal
import io
import configparser

sys.path.append('modules')

class Lemmy:
    class NoConfigException(Exception):
        def __init__(self, missing_file):
            super().__init__(f'config/{missing_file}.ini does not exist (create it from {missing_file}.example.ini)')

    def __init__(self):
        # perform setup that should not be performed again (i.e. in a reload)
        self.client = discord.Client()

        # perform synchronous setup
        self.load_all_sync()

        # register events
        @self.client.event
        async def on_message(message):
            channel = message.channel

            if type(channel) == discord.channel.DMChannel:
                recipient = channel.recipient.name if message.author == channel.me else channel.me.name
            elif type(channel) == discord.channel.GroupChannel:   # bot users can't be in these (yet)
                recipient = channel.name or ', '.join( list( { user.name for user in message.channel.recipients }.union({ self.client.user.name }) - { message.author.name } ) )
            elif type(channel) == discord.channel.TextChannel:
                recipient = f'{channel.guild}#{channel.name}'

            extras_phrase = '📎' * len(message.attachments) + '📊' * len(message.embeds)
            extras_phrase = f' +{extras_phrase}' if extras_phrase else ''

            self.log(f'{message.author.name} => {recipient}{extras_phrase}: {message.content}')

            # pass the event to the modules
            for module_name, module in self.modules.items():
                context = self.get_context(message.channel)
                if module_name in context['manifest']:
                    await module.on_message(message)

        @self.client.event
        async def on_voice_state_update(member, before, after):
            # pass the event to the modules
            for module_name, module in self.modules.items():
                context = self.get_context(member)
                if module_name in context['manifest']:
                    await module.on_voice_state_update(member, before, after)

        @self.client.event
        async def on_ready():
            # perform asynchronous setup
            await self.load_all_async()

            # pass the event to the modules
            for _, module in self.modules.items():
                await module.on_ready()

            self.log('Logged in.')

        # log in
        self.log('Logging in...')

        # run the bot
        loop = asyncio.get_event_loop()

        # enable the bot to respond to SIGINT/SIGTERM (Unix only)
        try:
            loop.add_signal_handler(signal.SIGINT, lambda: asyncio.ensure_future(self.handle_sigint()))
            loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.ensure_future(self.handle_sigterm()))
        except NotImplementedError:
            pass   # Lemmy is running in Windows - nothing we can do

        try:
            loop.run_until_complete(self.client.start(self.config['token']))
        except KeyboardInterrupt:
            loop.run_until_complete(self.client.logout())
        finally:
            loop.close()

        # at this point the bot has shut down
        self.log('Shut down.')

    def log(self, message):
        output = '[{}] {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message)

        self.logger.info(output)

    def load_all_sync(self):
        self.load_config()
        self.load_modules()
        self.setup_logging()

    async def load_all_async(self):
        await self.load_playing_message()
        await self.announce_servers()

    def load_config(self):
        for config_file in ['lemmy', 'contexts']:
            if not os.path.isfile(f'config/{config_file}.ini'):
                raise Lemmy.NoConfigException(config_file)

        # load config
        self.config = configparser.ConfigParser()
        self.config.read('config/lemmy.ini')
        self.config = dict(self.config['Lemmy'])

        # post-process config
        self.config['admins'] = [ int(id) for id in self.config['admins'].split() ]

        # load contexts
        self.contexts = configparser.ConfigParser()
        self.contexts.read('config/contexts.ini')
        self.contexts = dict(self.contexts)
        for key in self.contexts.keys():
            self.contexts[key] = dict(self.contexts[key])

        # post-process contexts
        for context in self.contexts.keys():
            self.contexts[context]['manifest'] = self.contexts[context]['manifest'].split()

    def load_modules(self):
        self.modules = {}

        for module_class_name in self.contexts['DEFAULT']['manifest']:
            module = importlib.import_module(module_class_name.lower())
            importlib.reload(module)   # changes to the module will be loaded (for if this was called again while the bot is running)
            class_ = getattr(module, module_class_name)
            self.modules[module_class_name] = class_(self)

    async def load_playing_message(self):
        await self.client.change_presence(activity=discord.Game(
            name=self.config.get('message')
        ))

    async def announce_servers(self):
        servers = await self.client.fetch_guilds(limit=None).flatten()
        servers = sorted([ server.name for server in servers ])
        self.log('\n'.join(['Logging in to servers:'] + servers))

    def setup_logging(self):
        logging.basicConfig(format='%(message)s', level=logging.WARNING)

        self.logger = logging.getLogger('lemmy')
        self.logger.setLevel(logging.INFO)

        if self.config.get('log_file'):
            self.logger.addHandler(logging.FileHandler(self.config['log_file']))

    async def shutdown(self):
        self.log('Shutting down...')
        await self.client.logout()

    def get_context(self, context):
        if type(context) == discord.TextChannel:
            context = context.guild
        elif type(context) == discord.Member:
            context = context.guild

        context_id = str(context.id)

        relevant_section = context_id if context_id in self.contexts else 'DEFAULT'
        return self.contexts[relevant_section]

    def resolve_symbol(self, context):
        return self.get_context(context)['symbol']

    def chunk_text(self, text, chunk_length=2000, chunk_prefix='', chunk_suffix=''):
        rows = text.splitlines()

        # for the time being, we're only going to break on linebreaks
        if max([ len(row) for row in rows ]) + len(chunk_prefix) + len(chunk_suffix) > chunk_length:
            raise ValueError('one or more rows exceed 2000 characters (with prefix and suffix)')

        chunks = []
        while rows:
            if chunks and len(chunk_prefix + chunks[-1] + '\n' + rows[0] + chunk_suffix) <= chunk_length:
                chunks[-1] += '\n' + rows[0]
            else:
                chunks.append(rows[0])
            del rows[0]

        # append prefixes and suffixes
        for i in range(len(chunks)):
            chunks[i] = chunk_prefix + chunks[i] + chunk_suffix

        return chunks

    @staticmethod
    def make_table(elements, column_count=6):
        # if there are fewer elements to display than column_count, we need to reduce column_count to match
        if len(elements) < column_count:
            column_count = len(elements)

        # determine how many elements are in each column
        column_base_length = len(elements) // column_count
        column_extra_count = len(elements) % column_count
        column_lengths = [ column_base_length for _ in range(column_count) ]
        # add the extras to the end of the relevant columns
        for i in range(column_extra_count):
            column_lengths[i] += 1

        # assemble columns
        columns = []
        for column_index in range(len(column_lengths)):
            column_start_index = sum(column_lengths[:column_index])
            column_end_index = sum(column_lengths[:column_index + 1])
            columns.append(elements[column_start_index:column_end_index])

        # pad elements
        for i, column in enumerate(columns[:-1]):
            column_width = max([ len(element) for element in column ])
            for j, element in enumerate(column):
                columns[i][j] = element + ' ' * (column_width - len(element))

        # assemble rows
        rows = [ list(row) for row in zip_longest(*columns) ]

        # remove any Nones added by zip_longest from the last row
        while rows[-1][-1] is None:
            rows[-1].pop()

        # convert rows to text
        return '\n'.join([ '  '.join(row) for row in rows ])

    async def handle_sigint(self):
        self.log('Received SIGINT.')
        await self.shutdown()

    async def handle_sigterm(self):
        self.log('Received SIGTERM.')
        await self.shutdown()

    def to_discord_file(self, contents, file_name):
        if type(contents) == bytes:
            contents = io.BytesIO(contents)
        elif type(contents) == str:
            contents = io.StringIO(contents)

        return discord.File(fp=contents, filename=file_name)

    async def send_text_file(self, body, destination, file_name='text.txt', comment=None):
        file = self.to_discord_file(body, file_name)
        await destination.send(comment, file=file)

    async def get_webhook(self, channel, webhook_name='Lemmy'):
        return discord.utils.find(lambda x: x.name == webhook_name, await channel.webhooks()) or await channel.create_webhook(name=webhook_name)



if __name__ == '__main__':
    lemmy = Lemmy()
