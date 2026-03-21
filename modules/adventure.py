import sys
sys.path.append('..')
from module import Module

import discord
import asyncio

STORY = {
    'start': {
        'title': '🏰 The Forgotten Dungeon',
        'description': (
            'You stand at the entrance of a crumbling dungeon. '
            'Torchlight flickers from within, and a cold breeze carries the faint sound of whispers.\n\n'
            'Two passages stretch before you.'
        ),
        'color': 0x7289DA,
        'choices': [
            {'label': 'Take the left passage', 'emoji': '⬅️', 'next': 'left_passage'},
            {'label': 'Take the right passage', 'emoji': '➡️', 'next': 'right_passage'},
        ],
    },
    'left_passage': {
        'title': '🕸️ The Spider\'s Lair',
        'description': (
            'You creep down the left passage. Thick webs cling to the walls. '
            'A giant spider descends from the ceiling, blocking your path!\n\n'
            'What do you do?'
        ),
        'color': 0x992D22,
        'choices': [
            {'label': 'Fight the spider', 'emoji': '⚔️', 'next': 'fight_spider'},
            {'label': 'Try to sneak past', 'emoji': '🤫', 'next': 'sneak_spider'},
        ],
    },
    'right_passage': {
        'title': '✨ The Enchanted Chamber',
        'description': (
            'The right passage opens into a shimmering chamber. '
            'A ghostly figure hovers over a treasure chest, guarding it silently.\n\n'
            'What do you do?'
        ),
        'color': 0x1F8B4C,
        'choices': [
            {'label': 'Speak to the ghost', 'emoji': '👻', 'next': 'speak_ghost'},
            {'label': 'Grab the chest and run', 'emoji': '💰', 'next': 'grab_chest'},
        ],
    },
    'fight_spider': {
        'title': '⚔️ Victory!',
        'description': (
            'You draw your blade and strike true! The spider recoils and skitters into the darkness. '
            'Behind where it stood, you find a gleaming golden key.\n\n'
            '🔑 **You win!** The key unlocks the dungeon\'s deepest vault. Glory and riches await!'
        ),
        'color': 0xF1C40F,
        'choices': [],
    },
    'sneak_spider': {
        'title': '🪦 Caught!',
        'description': (
            'You tiptoe carefully... but your foot catches a strand of web. '
            'The spider whips around and wraps you in silk before you can react.\n\n'
            '💀 **Game over.** You became a snack.'
        ),
        'color': 0x71368A,
        'choices': [],
    },
    'speak_ghost': {
        'title': '👻 The Ghost\'s Riddle',
        'description': (
            '"Brave soul," the ghost rasps. "Answer my riddle and the treasure is yours: '
            '*I have cities, but no houses. I have mountains, but no trees. '
            'I have water, but no fish. What am I?*"\n\n'
            'What do you answer?'
        ),
        'color': 0x3498DB,
        'choices': [
            {'label': 'A map', 'emoji': '🗺️', 'next': 'riddle_correct'},
            {'label': 'A painting', 'emoji': '🖼️', 'next': 'riddle_wrong'},
        ],
    },
    'grab_chest': {
        'title': '💀 Cursed!',
        'description': (
            'You lunge for the chest, but the ghost shrieks and the chest dissolves into smoke. '
            'A terrible curse washes over you — your legs turn to stone.\n\n'
            '💀 **Game over.** Greed was your downfall.'
        ),
        'color': 0xE74C3C,
        'choices': [],
    },
    'riddle_correct': {
        'title': '🗺️ Correct!',
        'description': (
            'The ghost smiles and fades away. The chest clicks open, revealing piles of ancient gold '
            'and a legendary sword wreathed in blue flame.\n\n'
            '🏆 **You win!** You leave the dungeon a hero and a legend.'
        ),
        'color': 0xF1C40F,
        'choices': [],
    },
    'riddle_wrong': {
        'title': '🖼️ Incorrect...',
        'description': (
            'The ghost lets out a mournful wail. "Wrong!" The chamber begins to collapse around you. '
            'You barely escape with your life, but the treasure is lost forever.\n\n'
            '😔 **You survived, but left empty-handed.**'
        ),
        'color': 0x95A5A6,
        'choices': [],
    },
}


class AdventureView(discord.ui.View):
    def __init__(self, scene_key, user_id):
        super().__init__(timeout=120)
        self.user_id = user_id
        scene = STORY[scene_key]
        for i, choice in enumerate(scene['choices']):
            button = discord.ui.Button(
                label=choice['label'],
                emoji=choice['emoji'],
                style=discord.ButtonStyle.primary,
                custom_id=f'adventure:{choice["next"]}:{user_id}',
            )
            button.callback = self._make_callback(choice['next'])
            self.add_item(button)

    def _make_callback(self, next_key):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message('This isn\'t your adventure!', ephemeral=True)
                return
            scene = STORY[next_key]
            embed = build_embed(scene, interaction.user)
            view = AdventureView(next_key, self.user_id) if scene['choices'] else None
            await interaction.response.edit_message(embed=embed, view=view)
            self.stop()
        return callback

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True


def build_embed(scene, user):
    embed = discord.Embed(
        title=scene['title'],
        description=scene['description'],
        color=scene['color'],
    )
    embed.set_footer(text=f'Adventurer: {user.display_name}')
    return embed


class Adventure(Module):
    docs = {
        'description': 'A short choose-your-own-adventure game'
    }

    docs_adventure = {
        'description': 'Begin a choose-your-own-adventure in the dungeon',
    }
    async def cmd_adventure(self, message, args, kwargs):
        scene = STORY['start']
        embed = build_embed(scene, message.author)
        view = AdventureView('start', message.author.id)
        await message.channel.send(embed=embed, view=view)
