from ddict import ddict

class LemmyConstants:
	def __init__(self):
		self.error = ddict()
		self.error.symbol = ":no_entry_sign:"
		self.error.notMod = "User must be moderator or above to perform this action."
		self.error.notAdmin = "User must be administrator to perform this action."