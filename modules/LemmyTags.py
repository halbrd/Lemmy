import json

class LemmyTags:
	def __init__(self):
		self.db = None
		self.converter = None

		try:
			with open("db/tagDb.json", "r") as f:
				self.db = json.load(f)
		except Exception as e:
			print("ERROR loading tagDb! (" + str(e) + ")")
		else:
			print("tagDb loaded with " + str(len(self.db)) + " tags.")

		try:
			with open("db/tagConverter.json", "r") as f:
				self.converter = json.load(f)
		except Exception as e:
			print("ERROR loading tagConverter! (" + str(e) + ")")
		else:
			print("tagConverter loaded with " + str(len(self.converter)) + " tags.")