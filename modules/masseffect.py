import sys
sys.path.append('..')
from module import Module

import random

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
          suffix = 'is not a class' if len(invalid_classes) == 1 else 'are not classes'
          await self.send_error(message, comment=f'{"/".join(invalid_classes)} {suffix}')
          return

      class_ = random.choice(classes)
      choice = random.choice(MassEffect.classes[class_])

      await message.channel.send(f'{choice} {class_}')
