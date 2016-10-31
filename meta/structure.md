# Project Structure
* `/data` is for all and only instantial data; deleting `/data` should "factory reset" the bot
* `/system` is for the code that runs Lemmy; updating Lemmy should only change `/system` (refactoring that changes how data is stored is an undecided grey area)
* `/res` is for data that isn't instantial but doesn't belong in code (eg. lenny faces)
* `/meta` is for internal documentation on the project
* `/old` is for code that I wrote that isn't going to be used but might be useful for reference

# Config
* Lemmy will use a carefully structured, centralised config system of JSON files
* The hierarchy will be roughly:

```bash
/global   #server-agnostic config
	some-global-config-topic.json
	some-global-config-topic.json
/<server id>   #server-specific config
	some-server-specific-topic.json
	some-server-specific-topic.json
	some-server-specific-topic.json
```

* Specifics to be determined (eg. do plugins get their own section?)
	* Update to above: I think plugins should get their own folder
* All config files will be written with pretty formatting (tabs and linebreaks) so that the user can edit them with a text editor
* There will also be a command for config mutation
* For config read/write, a nonexistent file should be created and initialized
* All commands will have mandatory metadata
	* Quick summary (using native docstrings and function.__doc__ call)
	* Detailed explanation (probably an explicit metadata field)
	* Usage (documenting all parameters and flags)
* Certain terminology should be global for standardization - e.g.:

```python
config.remove = ["delete", "del", "remove", "rem", "rm"]

if flag in config.remove:
	...
```
