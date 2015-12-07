password = "arbiter1"

import sys
sys.path.append('modules')

import discord
import re
import random
import reminder
import datetime
from randomLenny import randomLenny
import urllib
import os.path
from os import listdir
from os.path import isfile, join
from FloodProtector import FloodProtector
from CallLogger import CallLogger

client = discord.Client()
client.login('halbrd@outlook.com', password)

lenny = "( ͡° ͜ʖ ͡°)"

lennies = ["""░░░░░░░░░░░░▄▄▄▄░░░░░░░░░░░░░░░░░░░░░░░▄▄▄▄▄
░░░█░░░░▄▀█▀▀▄░░▀▀▀▄░░░░▐█░░░░░░░░░▄▀█▀▀▄░░░▀█▄
░░█░░░░▀░▐▌░░▐▌░░░░░▀░░░▐█░░░░░░░░▀░▐▌░░▐▌░░░░█▀
░▐▌░░░░░░░▀▄▄▀░░░░░░░░░░▐█▄▄░░░░░░░░░▀▄▄▀░░░░░▐▌
░█░░░░░░░░░░░░░░░░░░░░░░░░░▀█░░░░░░░░░░░░░░░░░░█
▐█░░░░░░░░░░░░░░░░░░░░░░░░░░█▌░░░░░░░░░░░░░░░░░█
▐█░░░░░░░░░░░░░░░░░░░░░░░░░░█▌░░░░░░░░░░░░░░░░░█
░█░░░░░░░░░░░░░░░░░░░░█▄░░░▄█░░░░░░░░░░░░░░░░░░█
░▐▌░░░░░░░░░░░░░░░░░░░░▀███▀░░░░░░░░░░░░░░░░░░▐▌
░░█░░░░░░░░░░░░░░░░░▀▄░░░░░░░░░░▄▀░░░░░░░░░░░░█
░░░█░░░░░░░░░░░░░░░░░░▀▄▄▄▄▄▄▄▀▀░░░░░░░░░░░░░█""", "ヽ( ͡° ͜ʖ ͡°)ﾉ", "( ͡° ͜ʖ ͡°)", "( ͠° ͟ʖ ͡°)", "ᕦ( ͡° ͜ʖ ͡°)ᕤ", "( ͡~ ͜ʖ ͡°)", "( ͡o ͜ʖ ͡o)", "͡° ͜ʖ ͡ -", "( ͡͡ ° ͜ ʖ ͡ °)﻿", "( ͡ ͡° ͡°  ʖ ͡° ͡°)", "(ง ͠° ͟ل͜ ͡°)ง", "( ͡° ͜ʖ ͡ °)", "(ʖ ͜° ͜ʖ)", "[ ͡° ͜ʖ ͡°]", "( ͡o ͜ʖ ͡o)", "{ ͡• ͜ʖ ͡•}", "( ͡° ͜V ͡°)", "( ͡^ ͜ʖ ͡^)", "( ‾ʖ̫‾)", "( ͡°╭͜ʖ╮͡° )", "ᕦ( ͡°╭͜ʖ╮͡° )ᕤ", "(σ ͟ʖσ)", "( ͡°ل͜ ͡°)", "(⚆ ͜ʖ⚆)", "( ͡°⍘ ͡°)", "(´• ͜ʖ •`)", "(Ȍ ͜ʖȌ)", "(❍⍘❍)", "( ͡°‿‿ ͡°)", "(☞ ͡° ͜ʖ ͡°)☞", "(づ ͡° ͜ʖ ͡°)づ", "(☞๏ ͜ʖ๏)☞", "(   ͡ °   ͜ ʖ   ͡ ° )", "(ಠ ͜ʖ ಠ)"]

BTS = None
roleList = []

fpLenny = FloodProtector(3)
fpEmotes = FloodProtector(3)
fpRuseman = FloodProtector(5)
clLogger = None

gameMembers = {
    "csgo": ["Chesty", "Dragons_Ire", "halbrd", "hugo", "KunhaiG", "Reginald"],
    "lol": ["Chesty", "Dragons_Ire", "EmeB", "halbrd", "KunhaiG", "LuckyLachy", "Solo Top Line"],
    "contagion": ["Dragons_Ire", "halbrd", "LuckyLachy", "RikerZZZ"],
    "rotr": ["RikerZZZ"],
    "sc2": ["halbrd", "KunhaiG", "LuckyLachy", "RikerZZZ", "Solo Top Line"],
    "borderlands": ["EmeB", "halbrd", "KunhaiG", "LuckyLachy"],
    "payday": ["Chesty", "halbrd", "KunhaiG", "LuckyLachy"],
    "test": ["halbrd", "Lemmy"]
}
gameNameConversion = {
    "csgo": "CS:GO",
    "lol": "League of Legends",
    "contagion": "Contagion",
    "rotr": "Rise of the Reds. Kappa.",
    "sc2": "Starcraft 2",
    "borderlands": "Borderlands 2",
    "payday": "Payday 2",
    "test": "Test"
}

emotes = [ os.path.splitext(f)[0] for f in listdir("pics/emotes") if isfile(join("pics/emotes",f)) ]
stickers = [ os.path.splitext(f)[0] for f in listdir("pics/stickers") if isfile(join("pics/stickers",f)) ]

def BecomeUser(user):
    client.edit_profile(password, username=user.name)

def BecomeLemmy():
    client.edit_profile(password, username="Lemmy")

@client.event
def on_message(msg):
    print("[" + msg.author.name + "|" + msg.channel.name + "|" + str(datetime.datetime.now().time()) + "] " + msg.content)

    jamesMatch = "("
    for group in gameMembers:
        jamesMatch += group + "|"
    if jamesMatch[-1] == "|":
        jamesMatch = jamesMatch[:-1]
    jamesMatch += ")"

    userMatch = "("
    for user in BTS.members:
        userMatch += user.name + "|"
    userMatch = userMatch[:-1] + ")"

    channelMatch = "("
    for channel in BTS.channels:
        #if channel.type == "text":
        channelMatch += channel.name + "|"
    channelMatch = channelMatch[:-1] + ")"

    isEmote = msg.content in emotes and msg.author != client.user
    isSticker = msg.content in stickers and msg.author != client.user

    if isEmote or isSticker:
        if fpEmotes.Ready(msg.author.name):
            # Disabled
            #BecomeUser(msg.author)

            client.send_message(msg.channel, "__**" + msg.author.name + "**__")

            subFolder = ("emotes" if isEmote else "stickers")
            directory = "pics/" + subFolder + "/"

            client.send_file(msg.channel, directory + msg.content + ".png")
            fpEmotes.Sent(msg.author.name)

            # Disabled 
            #BecomeLemmy()

        client.delete_message(msg)

    if re.match("!f5(?!\S)", msg.content):
        client.send_message(msg.channel, "Nice try, nerd.")

    elif re.match("!help(?!\S)", msg.content):
        # with open("help.txt") as f:
        #     helpText = f.read()
        # client.send_message(msg.channel, "```\n~~~ Lemmy Command Reference ~~~\n" + helpText + "```"

        client.send_message(msg.channel, "http://lynq.me/lemmy/")

    elif re.match("!emotes(?!\S)", msg.content):
        #client.send_message(msg.channel, "```\n" + ", ".join(emotes) + "\n\n\nType !stickers to view a list of available stickers.```")
        client.send_message(msg.channel, "http://lynq.me/lemmy/#emotes")

    elif re.match("!stickers(?!\S)", msg.content):
        #client.send_message(msg.channel, "```\n" + ", ".join(stickers) + "\n\n\nType !emotes to view a list of available emotes.```")
        client.send_message(msg.channel, "http://lynq.me/lemmy/#stickers")

    elif re.match("!lenny(?!\S)", msg.content):
        if fpLenny.Ready(msg.author.name):
            msgLenny = ""
            msgPrefix = ""
            rare = False

            if re.search(" -og", msg.content):
                msgLenny = lenny
            
            elif re.search(" -r", msg.content):
                msgLenny = randomLenny()

            elif re.search(" -.+", msg.content):
                msgLenny = "*Flag not recognized.*\n"
            
            else:
                # Random index
                index = random.randint(0, len(lennies)-1)

                # If the rare lenny was rolled, roll again
                # if index == 0:
                #     index = random.randint(0, 10)

                # If message is from the testing channel, pick rare lenny
                # if msg.channel.name == "rarelennytest":
                #     index = 0
                
                # Set rare to true if the rare lenny was rolled
                # rare = (index == 0)

                msgLenny = lennies[index]

            client.send_message(msg.channel, msgPrefix + msgLenny)
            fpLenny.Sent(msg.author.name)

            #if rare:
            #    client.send_message(msg.channel, "Congratulations, " + msg.author.mention() + ", you found the exceedingly rare Lenny!")

        else:
            client.delete_message(msg)

    elif re.match("!correct(?!\S)", msg.content):
        client.send_message(msg.channel, "https://youtu.be/OoZN3CAVczs")

    elif re.match("!refresh(?!\S)", msg.content) or re.match("!F5(?!\S)", msg.content):
        # Check emotes
        global emotes, stickers
        refreshedEmotes = [ os.path.splitext(f)[0] for f in listdir("pics/emotes") if isfile(join("pics/emotes",f)) ]
        refreshedStickers = [ os.path.splitext(f)[0] for f in listdir("pics/stickers") if isfile(join("pics/stickers",f)) ]

        newEmotes = [item for item in refreshedEmotes if item not in emotes]
        newStickers = [item for item in refreshedStickers if item not in stickers]

        emotes = refreshedEmotes
        stickers = refreshedStickers

        if len(newEmotes) > 0:
            #client.send_message(msg.channel, "New emotes: " + ", ".join(newEmotes))
            client.send_message(msg.channel, "__New emotes:__")

            for emote in newEmotes:
                client.send_message(msg.channel, emote)
                client.send_file(msg.channel, "pics/emotes/" + emote + ".png")

        if len(newStickers) > 0:
            #client.send_message(msg.channel, "New stickers: " + ", ".join(newStickers))
            client.send_message(msg.channel, "__New stickers:__")

            for sticker in newStickers:
                client.send_message(msg.channel, sticker)
                client.send_file(msg.channel, "pics/stickers/" + sticker + ".png")

        client.delete_message(msg)

    elif re.match("!8ball .+", msg.content):
        responses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes, definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]

        client.send_message(msg.channel, msg.author.mention() + " :8ball: " + responses[random.randint(0, len(responses)-1)])

    elif re.match("!userinfo " + userMatch, msg.content):
        givenName = msg.content[10:]
        user = discord.utils.find(lambda m: m.name == givenName, msg.channel.server.members)
        client.send_message(msg.channel, "**Username:** " + user.name + "\n**ID:** " + user.id + "\n**Avatar URL:** " + user.avatar_url())

    elif re.match("!channelinfo " + channelMatch, msg.content):
        channel = discord.utils.find(lambda m: m.name == msg.content[13:], [x for x in msg.channel.server.channels if x.type == "text"])
        client.send_message(msg.channel, "**Channel name: **" + channel.name + "\n**ID: **" + channel.id)

    elif re.match("!james ", msg.content):
        if re.search(" -tags", msg.content):
            response = "```"
            for key in gameMembers:
                response += "\n" + key + " (" + gameNameConversion[key] + ")"
                for member in gameMembers[key]:
                    response += "\n> " + member
                response += "\n"
            response += "```"
            client.send_message(msg.channel, response)

        elif re.match("!james " + jamesMatch, msg.content):
            gameTag = msg.content[7:]
            response = "Pinging "
            for username in gameMembers[gameTag]:
                user = discord.utils.find(lambda m: m.name == username, msg.channel.server.members)
                if user is not None:
                    response += user.mention() + " "
            response += "for " + gameNameConversion[gameTag]
            client.send_message(msg.channel, response)

    elif re.match("!isLennySentient(?!\S)", msg.content):
        client.send_message(msg.channel, "No." if random.randint(0, 499) != 0 else "Yes.")

    # elif re.match("!ruseman(?!\S", msg.content):
    #     if fpRuseman.Ready(msg.author.name):
    #         memes = []
    #         for path, subdirs, files in os.walk("pics/ruseman/"):
    #             for name in files:
    #                 print(name)
    #                 memes.append(name)
            
    #         fpRuseman.Sent(msg.author.name)

    #         client.send_file(msg.channel, "pics/ruseman/" + memes[random.randint(0, len(memes)-1)])
    #     else:
    #         client.delete_message(msg)

@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------\n')

    global BTS, roleList

    for server in client.servers:
        if server.name == "Better Than Skype":
            BTS = server
            print("BTS found\n")
            global clLogger
            clLogger = CallLogger(BTS.channels)

    if BTS:
        for role in BTS.roles:
            if role.name != "@everyone":
                roleList.append(role.name)
        print("Role list: " + str(roleList) + "\n")

    global lemmyAvatar
    lemmyAvatar = client.user.avatar

    print("Waiting for messages.\n------\n")

@client.event
def on_voice_state_update(member):
    global BTS
    responses = clLogger.UpdateStatuses(BTS.channels)
    for response in responses:
        client.send_message(discord.utils.find(lambda m: m.name == "lemmybot", msg.channel.server.channels), "Call ended in " + response[0] + ", duration " + response[1])




client.run()
