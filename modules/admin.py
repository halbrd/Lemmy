import sys
sys.path.append('..')
from module import Module

import discord

class Admin(Module):
    docs = {
        'description': 'Provides useful commands for managing Discord servers'
    }

    # init

    async def on_reaction_add(self, reaction, user):
        billboard_message_ids = self.load_data(f'role_billboards_{reaction.message.channel.guild.id}', default='[]')

        message_id = reaction.message.id

        if not message_id in billboard_message_ids:
            print('message_id not in billboard_message_ids, return')
            return

        role_maps = self.load_data(f'role_map_{reaction.message.channel.guild.id}', default='[]')
        role_match = [ role for role in role_maps if role['emoji'] == reaction.emoji ]

        if not role_match:
            print(f'{reaction.emoji} not in {[ role["emoji"] for role in role_maps ]}')
            return

        role_match = role_match[0]

        role = reaction.message.channel.guild.get_role(role_match['role_id'])

        await reaction.message.channel.send(f'{user.name} should get {role.name}')

        await reaction.message.remove_reaction(reaction.emoji, user)


    docs_roles = {
        'description': 'Produces a self-service role-assignment dialog',
        'admin_only': True
    }
    async def cmd_roles(self, message, args, kwargs):
        role_maps = self.load_data(f'role_map_{message.channel.guild.id}', default='[]')

        embed = discord.Embed()
        embed.title = 'Peanut butter and jelly'
        embed.description = ''

        for role_map in role_maps:
            role = message.channel.guild.get_role(role_map['role_id'])
            embed.description += f'\n  {role_map["emoji"]}   {role.name}'

        billboard = await message.channel.send(embed=embed)

        for role_map in role_maps:
            await billboard.add_reaction(role_map['emoji'])

        billboard_message_ids = self.load_data(f'role_billboards_{message.channel.guild.id}', default='[]')
        billboard_message_ids = [ id for id in billboard_message_ids if not id == billboard.id ] + [billboard.id]
        self.save_data(f'role_billboards_{message.channel.guild.id}', billboard_message_ids)
