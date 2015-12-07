import datetime

class FloodProtector:
	def __init__(self, cooldown):
		self.db = {}
		self.cooldown = cooldown

	# Returns a boolean value indicating whether or not the id is "ready", ie. not on cooldown
	def Ready(self, id):
		if id not in self.db:
			return True
		else:
			timeDiff = datetime.datetime.now() - self.db[id]
			return timeDiff.total_seconds() > self.cooldown
	
	# Set id's last sent datetime to now
	def Sent(self, id):
		self.db[id] = datetime.datetime.now()