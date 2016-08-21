# Project Structure
* `/data` is for all and only instantial data; deleting `/data` should "factory reset" the bot
* `/system` is for the code that runs Lemmy; updating Lemmy should only change `/system` (refactoring that changes how data is stored is an undecided grey area)
* `/res` is for data that isn't instantial but doesn't belong in code (eg. lenny faces)
* `/meta` is for internal documentation on the project
* `/old` is for code that I wrote that isn't going to be used but might be useful for reference
