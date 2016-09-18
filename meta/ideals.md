# Design Ideals
## General
* Markdown is love, markdown is life

## Code structure
* Object orientation isn't too uncool to use yet, so we're going with it (and we're not using complicated inheritance so it doesn't matter anyway)
* Breaking things up into directories and files is better than large files
* Wherever possible, store things in JSON, not just lines in a text file
* Think big picture - reusable microframeworks over in-situ algorithms
* Until performance becomes an issue, Lemmy should read from file as required, rather than reading a file into memory, in order to achieve live updating 

## Code style
* Tabs
* Class names use CapsCase
* Variable and function names use camelCase
* Comments are good, but don't narrate the code; focus on the overall function of a block of code
* Comments on inputs/outputs of ambiguous functions are good
* Commit messages should be short but descriptive, and use present tense verbs (eg. `Implement !command`, `Fix !command not printing error message`, `Remove !command due to Skynet-related issues`)

## Tech stack
* JSON > everything else until we have large amounts of data and/or frequent read/write (we'll cross that bridge when we come to it)
* `pip` installed dependencies are fine, but they must be included in `/dependencies`

## Project management
* Feature branches and pull requests (a la Gitflow) should be used (though *responsibly* skipping this for things that you have very carefully checked is okay)
* [Trello board](https://trello.com/b/Nt0I1pZK/lemmy)

## User experience style
* Commands should be loosely based on Unix-style command structure (something like the `!command -flag parameter` thing we have going now but not quite)
	* For example: at the moment we have `!ccomm -del thing1 -del thing2 -del thing3`, but we should have `!ccomm -del thing1 thing2 thing3` (though the first would still work).

## Misc
These are just random, unrelated things that I want to document
* Lemmy will have core emotes that are built in and hosted externally (to keep repo size down), though an option to download them all locally for improved performance is a good idea. An instance of Lemmy will also be able to have its own emotes that are stored locally.
* Modules should probably have metadata for attribution and other info.
* I'd really like to have a "terminal mode" where all of your messages are interpreted as commands, without needing to prepend a symbol (i.e. `!`)
