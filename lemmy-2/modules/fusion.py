import sys
sys.path.append('..')
from module import Module

import random
import requests
import discord

class Fusion(Module):
    docs = {
        'description': 'Pokémon Fusion'
    }

    pokemon_codes = {
        'bulbasaur': 1, 'ivysaur': 2, 'venusaur': 3, 'charmander': 4, 'charmeleon': 5, 'charizard': 6, 'squirtle': 7,
        'wartortle': 8, 'blastoise': 9, 'caterpie': 10, 'metapod': 11, 'butterfree': 12, 'weedle': 13, 'kakuna': 14,
        'beedrill': 15, 'pidgey': 16, 'pidgeotto': 17, 'pidgeot': 18, 'rattata': 19, 'raticate': 20, 'spearow': 21,
        'fearow': 22, 'ekans': 23, 'arbok': 24, 'pikachu': 25, 'raichu': 26, 'sandshrew': 27, 'sandslash': 28,
        'nidoranf': 29, 'nidorina': 30, 'nidoqueen': 31, 'nidoranm': 32, 'nidorino': 33, 'nidoking': 34,
        'clefairy': 35, 'clefable': 36, 'vulpix': 37, 'ninetales': 38, 'jigglypuff': 39, 'wigglytuff': 40, 'zubat': 41,
        'golbat': 42, 'oddish': 43, 'gloom': 44, 'vileplume': 45, 'paras': 46, 'parasect': 47, 'venonat': 48,
        'venomoth': 49, 'diglett': 50, 'dugtrio': 51, 'meowth': 52, 'persian': 53, 'psyduck': 54, 'golduck': 55,
        'mankey': 56, 'primeape': 57, 'growlithe': 58, 'arcanine': 59, 'poliwag': 60, 'poliwhirl': 61, 'poliwrath': 62,
        'abra': 63, 'kadabra': 64, 'alakazam': 65, 'machop': 66, 'machoke': 67, 'machamp': 68, 'bellsprout': 69,
        'weepinbell': 70, 'victreebel': 71, 'tentacool': 72, 'tentacruel': 73, 'geodude': 74, 'graveler': 75,
        'golem': 76, 'ponyta': 77, 'rapidash': 78, 'slowpoke': 79, 'slowbro': 80, 'magnemite': 81, 'magneton': 82,
        'farfetchd': 83, 'doduo': 84, 'dodrio': 85, 'seel': 86, 'dewgong': 87, 'grimer': 88, 'muk': 89, 'shellder': 90,
        'cloyster': 91, 'gastly': 92, 'haunter': 93, 'gengar': 94, 'onix': 95, 'drowzee': 96, 'hypno': 97, 'krabby': 98,
        'kingler': 99, 'voltorb': 100, 'electrode': 101, 'exeggcute': 102, 'exeggutor': 103, 'cubone': 104,
        'marowak': 105, 'hitmonlee': 106, 'hitmonchan': 107, 'lickitung': 108, 'koffing': 109, 'weezing': 110,
        'rhyhorn': 111, 'rhydon': 112, 'chansey': 113, 'tangela': 114, 'kangaskhan': 115, 'horsea': 116, 'seadra': 117,
        'goldeen': 118, 'seaking': 119, 'staryu': 120, 'starmie': 121, 'mrmime': 122, 'scyther': 123, 'jynx': 124,
        'electabuzz': 125, 'magmar': 126, 'pinsir': 127, 'tauros': 128, 'magikarp': 129, 'gyarados': 130, 'lapras': 131,
        'ditto': 132, 'eevee': 133, 'vaporeon': 134, 'jolteon': 135, 'flareon': 136, 'porygon': 137, 'omanyte': 138,
        'omastar': 139, 'kabuto': 140, 'kabutops': 141, 'aerodactyl': 142, 'snorlax': 143, 'articuno': 144,
        'zapdos': 145, 'moltres': 146, 'dratini': 147, 'dragonair': 148, 'dragonite': 149, 'mewtwo': 150, 'mew': 151,
    }

    docs_fusion = {
        'description': 'Fuses Pokémon together',
        'usage': 'fusion <first pokemon or "?"> <second pokemon or "?">',
        'examples': [
            'fusion shellder voltorb',
            'fusion nidoranf mrmime',
            'fusion Nidoran-F "Mr. Mime"',
            'fusion tangela ?'
        ]
    }
    async def cmd_fusion(self, message, args, kwargs):
        if len(args) != 2:
            raise Module.CommandError

        def interpret(input):
            if input == '?':
                input = random.choice(list(Fusion.pokemon_codes.keys()))

            letters = set('abcdefghijklmnopqrstuvwxyz')
            return ''.join(map(lambda char: char if char in letters else '', input.lower()))

        first_code = Fusion.pokemon_codes.get(interpret(args[0]))
        second_code = Fusion.pokemon_codes.get(interpret(args[1]))

        if first_code is None and second_code is None:
            await self.send_error(message, comment='neither of those are Gen. 1 Pokémon')
            return
        elif first_code is None:
            await self.send_error(message, comment=f'\'{args[0]}\' is not a Gen. 1 Pokémon')
            return
        elif second_code is None:
            await self.send_error(message, comment=f'\'{args[1]}\' is not a Gen. 1 Pokémon')
            return

        page_url = f'https://pokemon.alexonsager.net/{first_code}/{second_code}'
        page = requests.get(page_url).text

        # this HTML wrangling is manual for performance reasons
        def extract(page, id, left_border, right_border):
            '''
            page -- webpage HTML as string
            id -- the HTML id of the element containing the target text
            left_border -- the text that will immediately precede the target text, and appear only once between the id
                and the target text
            right_border -- the text that will immediately succeed the target text
            '''
            id = f'id="{id}"'
            id_index = page.find(id)
            slice_start = page.find(left_border, id_index + len(id)) + len(left_border)
            slice_end = page.find(right_border, slice_start)
            target_text = page[slice_start:slice_end]

            return target_text

        name = extract(page, 'pk_name', '>', '<')
        image = extract(page, 'pk_img', 'src=', ' />')

        await message.channel.send(
            embed=discord.Embed(
                title=name,
                url=page_url
            ).set_image(url=image)
        )
