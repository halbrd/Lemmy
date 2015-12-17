class Vote:
	def __init__(self, question, answers):
		self.question = question
		self.answers = answers
		self.votes = [0 for _ in answers]

	def AddVote(self, index):
		if index > 1 and index < len(votes) + 1:
			self.votes[index - 1] += 1
		else:
			raise IndexError("Given index outside range of answers")

	def __str__(self):
		maxVotes = max(self.votes)

		ret = "```\n"
		ret += self.question + "\n"
		for _ in range(len(self.question)):
			ret += "-"
		ret += "\n"
		for i in range(len(self.answers)):
			ret += i + ". " + self.answers[i] + "\n"
			ret += "|"
			for _ in range(self.votes[i]):
				ret += "="
			for _ in range(maxVotes - self.votes[i]):
				ret += " "
			ret += "|\n\n"
		ret += "```"
		return ret