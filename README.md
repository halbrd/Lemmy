# Lemmy
Your friendly neighbourhood Discord bot

Note: Lemmy is being re-written in /lemmy-2. The new codebase is much nicer.

# Lemmy Reference Page
Reference for the non-technical side of Lemmy can be found at http://lynq.me/lemmy/

# Lemmy Basics
LemmyBot.py - The central class that is Lemmy

RunLemmy.py - A simple script that creates an instance of Lemmy and activates it

LemmyCommands.py - The collection of functions that commands call

LemmyResources.py - The class that stores (references to) all "resources" - eg. Lennies and emotes/stickers

LemmyUtils.py - A collection of useful functions used within LemmyBot

LemmyRadio.py - The code that runs the music playing part of Lemmy

LemmyConstants.py - Constant strings for global use - designed to increase consistency with error messages and make changes easy

LemmyTags.py - Controller for the tag functionality (more commonly known as !james)

LemmyConfig.py - A centralized settings section - makes customizing Lemmy easy and helps Lemmy to be server-agnostic



/archive - Old files kept for one reason or another

/db - Files that are generally "databasey"

/modules - Non-central imported Python files used by Lemmy

/pics - Images used by Lemmy

# Lemmy Licence
Um... You can use Lemmy's code if you want. Just attribute somewhere if you copy lots of it and don't use it for evil.
