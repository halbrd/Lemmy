# Design Ideals
## General
* Markdown is love, markdown is life

## Code structure
* Object orientation isn't too uncool to use yet, so we're going with it (and we're not using complicated inheritance so it doesn't matter anyway)
* Breaking things up into directories and files is better than large files
* Wherever possible, store things in JSON, not just lines in a text file
* Think big picture - reusable microframeworks over in-situ algorithms
* For config read/write, a nonexistent file should be created and initialized

## Code style
* Tabs
* Class and function names use CapsCase
* Variable names use camelCase
* Comments are good, but don't narrate the code; focus on the overall function of a block of code
* Comments on inputs/outputs of ambiguous functions are good

## Tech stack
* JSON > everything else until we have large amounts of data and/or frequent read/write (we'll cross that bridge when we come to it)
* `pip` installed dependencies are fine, but they must be included in `/dependencies`

## Project management
* Feature branches and pull requests (a la Gitflow) should be used (though *responsibly* skipping this for things that you have very carefully checked is okay)
* [Trello board](https://trello.com/b/Nt0I1pZK/lemmy)
