"""
Required docstrings (FIT1008 lelelelelelelelele):
@input (params)
@function (description of what it does)
@output (resultant actions and/or return value)
"""

def TitleBox(string):
	"""
	@input: Text to be title-ified
	@function: Turn input string into highlighted title box
	@output: Title-box'd version of the strings (with linebreaks above and below, for convenience)
	"""
	return "\n" + "".join(["=" for _ in range(len(string) + 4)]) + "\n= " + string + " =\n" + "".join(["=" for _ in range(len(string) + 4)]) + "\n"

