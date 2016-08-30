# Project Terminology
* **command symbol** - the symbol that prefixes commands as called in Discord (usually `!`)
* **command** - a particular function that a user calls from Discord
  * e.g. `!command`
* **flag** - a "sub-command" of a command, prefixed by a hyphen
  * e.g. `!command -flag`
* **parameter** or **param** - a value that is passed to a command
  * **command param** - a parameter immediately following the command invocation or another command param
    * e.g. `!command commandParam1 commandParam2`
  * **flag param** - a parameter immediately following the command invocation or another command param (should have relevance only to that flag)
    * e.g. `!command -flag flagParam1 flagParam2`
