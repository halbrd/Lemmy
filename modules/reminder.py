import datetime

def MonthDaySuffix(monthDay):
	if monthDay % 10 == 1:
		return "st"
	elif monthDay % 10 == 2:
		return "nd"
	elif monthDay % 10 == 3:
		return "rd"
	else:
		return "th"

class Reminder:
	def __init__(self, author, channel, setDateTime, triggerDateTime, message):
		self.author = author
		self.channel = channel
		self.message = message
		self.setDateTime = setDateTime
		self.targetDateTime = targetDateTime

	def Check(self):
		if self.targetDateTime >= datetime.datetime.now():
			suffix = MonthDaySuffix(setDateTime.date.day())
			message = "@" + self.author + ", your reminder from " + self.setDateTime.strftime("%A, %d") + suffix + self.setDateTime.strftime(" %B, %Y") + " has been triggered."
			if self.message: message += '\n"' + self.message + '"'
			return message
		else:
			return False

class ReminderManager:
	def __init__(self):
		self.reminders = []

	def NewReminder(self, author, channel, setDateTime, triggerDateTime, message):
		self.reminders.append(Reminder(author, channel, setDateTime, triggerDateTime, message))

	def CheckAll(self):
		done = [reminder.Check() for reminder in self.reminders if reminder.Check()]
		self.reminders = [reminder for reminder in self.reminders if not reminder.Check()]

		return done

	def ParseCommand(self, command, author, channel, setDateTime):
		literalDate = re.search("\d\d\d\d-\d\d-\d\d", command).group(0)
		offsetDate = re.search("\d+ (seconds|minutes|hours|days|weeks|months) from now").group(0)

		if literalDate and not offsetDate:
			try:
				triggerDateTime = datetime.strptime(literalDate, "%Y-%m-%d")
			except:
				return False

		elif offsetDate and not literalDate:
			amount = re.match("\d+", offsetDate)
			interval = re.search("(seconds|minutes|hours|days|weeks|months)", offsetDate)
			
			if interval == "seconds": timeDelta = datetime.timedelta(seconds=amount)
			if interval == "minutes": timeDelta = datetime.timedelta(minutes=amount)
			if interval == "hours": timeDelta = datetime.timedelta(hours=amount)
			if interval == "days": timeDelta = datetime.timedelta(days=amount)
			if interval == "weeks": timeDelta = datetime.timedelta(weeks=amount)
			if interval == "months": timeDelta = datetime.timedelta(months=amount)
			
			triggerDateTime = setDateTime + timeDelta

		else:
			return False

		# At this point we have a valid date
		message = re.search("""('|")(.|\n)*('|")""", command)
		if message: message = message.group(0)

		self.NewReminder(author, channel, setDateTime, triggerDateTime, message)
		return triggerDateTime