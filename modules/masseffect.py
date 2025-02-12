import sys
sys.path.append('..')
from module import Module

import random
import re

class MassEffect(Module):
    docs = {
        'description': 'Does stuff related to Mass Effect games'
    }

    classes_in_order = ['Adept', 'Soldier', 'Engineer', 'Sentinel', 'Infiltrator', 'Vanguard']

    classes = {
        'Adept': ['Human Male', 'Human Female', 'Asari', 'Drell', 'Asari Justicar', 'Ex-Cerberus', 'N7 Fury', 'Volus', 'Krogan Shaman', 'Batarian Slasher', 'Awakened Collector'],
        'Soldier': ['Human Male', 'Human Female', 'Krogan', 'Turian', 'Battlefield 3', 'Batarian', 'Vorcha', 'N7 Destroyer', 'Turian Havoc', 'Geth Trooper', 'Quarian Marksman', 'Geth Juggernaut'],
        'Engineer': ['Human Male', 'Human Female', 'Quarian', 'Salarian', 'Geth', 'Quarian Male', 'N7 Demolisher', 'Volus', 'Vorcha Hunter', 'Turian Saboteur', 'Talon Mercenary'],
        'Sentinel': ['Human Male', 'Human Female', 'Turian', 'Krogan', 'Batarian', 'Vorcha', 'N7 Paladin', 'Volus Mercenary', 'Asari Valkyrie', 'Krogan Warlord'],
        'Infiltrator': ['Human Male', 'Human Female', 'Salarian', 'Quarian', 'Geth', 'Quarian Male', 'N7 Shadow', 'Turian Ghost', 'Asari Huntress', 'Drell Assassin', 'Alliance Infiltration Unit'],
        'Vanguard': ['Human Male', 'Human Female', 'Drell', 'Asari', 'Krogan Battlemaster', 'Ex-Cerberus', 'N7 Slayer', 'Volus Protector', 'Batarian Brawler', 'Cabal'],
    }

    def classes_as_strings():
        r = []
        for class_group, classes in MassEffect.classes.items():
            for class_ in classes:
                r.append(f'{class_} {class_group}')
        return r

    async def on_reaction_add(self, reaction, user):
        # don't respond to Lemmy's reactions
        if user.id == self.client.user.id:
            return

        # don't respond to anyone but Lemmy's messages
        if not reaction.message.author.id == self.client.user.id:
            return

        # don't reply unless it looks like a me3class invokation
        matches_pattern = re.fullmatch('<@\d+>( [\w/]+)?\n(~~[A-Za-z \-37]+~~\n)*[A-Za-z \-37]+', reaction.message.content)
        if not matches_pattern:
            return

        lines = reaction.message.content.split('\n')

        # get author mention and types selection
        author_mention = lines[0]
        types = None

        if ' ' in author_mention:
            types = author_mention.split(' ')[-1].split('/')
            author_mention = author_mention.split(' ')[0]

        # don't respond to reactions not from the original author
        author_id = author_mention.strip('<>@')
        if author_id != str(user.id):
            return

        last_used_class = lines[-1]

        previous_used_classes = [ x[2:-2] for x in lines[1:-1] ]

        used_classes = previous_used_classes + [last_used_class]

        unused_classes = [ x for x in MassEffect.classes_as_strings() if not x in used_classes ]

        # filter by types selection
        if types:
            unused_classes = [ x for x in unused_classes if any([ x.lower().endswith(type) for type in types ]) ]

        if len(unused_classes) == 0:
            new_class = '💩'
        else:
            new_class = random.choice(unused_classes)

        crossed_out_old_classes = [ f'~~{old_class}~~' for old_class in used_classes ]
        new_message = '\n'.join([lines[0]] + crossed_out_old_classes + [new_class])

        await reaction.message.edit(content=new_message)

    docs_me3class = {
        'description': 'Picks a Mass Effect 3 multiplayer class for you',
        'usage': 'me3class <class/class/...>',
        'examples': [ 'me3class', 'me3class adept', 'me3class sentinel/infiltrator/engineer' ],
    }
    async def cmd_me3class(self, message, args, kwargs):
        classes = MassEffect.classes_in_order

        if len(args) > 1:
            await self.send_error(message)
            return

        if len(args) == 1:
            classes = [ x.capitalize() for x in args[0].split('/') ]
            invalid_classes = [ x for x in classes if not x in MassEffect.classes_in_order ]

            if invalid_classes:
                suffix = 'is not a class type' if len(invalid_classes) == 1 else 'are not class types'
                await self.send_error(message, comment=f'{"/".join(invalid_classes)} {suffix}')
                return

        mention_types_slug = message.author.mention
        if len(args) == 1:
            mention_types_slug += ' ' + args[0].lower()

        class_ = random.choice(classes)
        choice = random.choice(MassEffect.classes[class_]) + ' ' + class_

        response = await message.channel.send(mention_types_slug + '\n' + choice)
        await response.add_reaction('🎲')
