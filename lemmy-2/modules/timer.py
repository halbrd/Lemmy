import sys
sys.path.append('..')
from module import Module

import datetime
import asyncio
import re
from decimal import Decimal   # BEGONE FLOAT
import dateparser

class Timer(Module):
	docs = {
		'description': 'Posts an alert after a specified time period'
	}

	TO_SECONDS = {   # the number to multiply a unit by to convert them into seconds
		's': 1,
		'm': 60,
		'h': 60 * 60,
		'd': 60 * 60 * 24,
		'w': 60 * 60 * 24 * 7,
		'y': 60 * 60 * 24 * 365
	}

	TO_WORD = {
		'y': 'year',
		'w': 'week',
		'd': 'day',
		'h': 'hour',
		'm': 'minute',
		's': 'second'
	}

	def seconds_to_natural_language(seconds):
		units = ['y', 'w', 'd', 'h', 'm', 's']
		terms = []

		for unit in units:
			quantity = seconds // Timer.TO_SECONDS[unit]
			seconds %= Timer.TO_SECONDS[unit]

			if quantity > 0:
				unit_word = Timer.TO_WORD[unit] + ('s' if quantity > 1 else '')
				terms.append(f'{int(quantity)} {unit_word}')

		return ', '.join(terms)

	def pythonize_timer(self, timer):
		print(f'id: {timer["creator"]}')
		timer['expiration'] = datetime.datetime.strptime(timer['expiration'], '%Y-%m-%d %H:%M:%S')
		timer['creator'] = self.client.get_user(timer['creator'])
		timer['destination'] = self.client.get_channel(timer['destination'])
		print(f'user: {timer["creator"]}')
		return timer

	def depythonize_timer(self, timer):
		timer['expiration'] = timer['expiration'].strftime('%Y-%m-%d %H:%M:%S')
		timer['creator'] = timer['creator'].id
		timer['destination'] = timer['destination'].id
		return timer

	def get_timers(self):
		timers = self.load_data('timers', default='[]')
		timers = list(map(self.pythonize_timer, timers))
		return timers

	def save_timers(self, timers):
		timers = list(map(self.depythonize_timer, self.timers))
		self.save_data('timers', timers)

	def add_timer(self, timer):
		self.timers.append(timer)
		self.save_timers(self.timers)

	async def on_ready(self):
		self.timers = self.get_timers()

		asyncio.get_event_loop().create_task(self.check_timers())

# timers = [
# 	{
# 		"creator": 123469284359287345,
# 		"expiration": "yyyy-MM-dd hh:mm:ss",
# 		"duration": "1 day, 2 hours, 3 minutes, 4 seconds",
# 		"message": "a something yes",   # or null
# 		"destination": 237462098173468765   # use client.get_channel(id)
# 	}
# ]

	async def check_timers(self):
		CHECK_INTERVAL = 1

		while True:
			to_delete = []

			# try:
			for i, timer in enumerate(self.timers):
				if datetime.datetime.now() >= timer['expiration']:
					message = f'{timer["creator"].mention} Your timer for {timer["duration"]} is up.'
					if timer['message']:
						message += f'\n`{timer["message"]}`'

					await timer['destination'].send(message)
					to_delete.append(i)

			# clean up expired timers
			for index in reversed(sorted(to_delete)):
				del self.timers[index]

			if len(to_delete) > 0:
				self.save_timers(self.timers)

			to_delete = []


			await asyncio.sleep(CHECK_INTERVAL)
			# except Exception as e:   # prevent an exception from killing the job
			#     logging.error(f'Exception in check_timers job: {type(exception).__name__}: {str(exception)}')
			#     continue


	docs_timer = {
		'description': 'Starts a countdown timer',
		'usage': 'timer <duration> <message>',
		'examples': [ 'timer 3s', 'timer 1d2h3m4s "1 day, 2 hours, 3 minutes, 4 seconds!"']
	}
	async def cmd_timer(self, message, args, kwargs):
		if not 1 <= len(args) <= 2:
			await self.send_error(message)
			return

		# TODO: delete this command

		self.add_timer({
			'creator': message.author,
			'destination': message.channel,
			'expiration': expiry,
			'duration': Timer.seconds_to_natural_language(duration_ms / 1000),
			'message': args[1] if len(args) > 1 else None
		})

		await message.add_reaction('✅')

	docs_remindme = {
		'description': 'Reminds the user of something at the specified time',
		'usage': 'remindme <activation date time> <message>',
		'examples': [
			'remindme "in 6 days, 7 hours" "to do something"',
			'remindme "2156-01-07" "Nic Cage turns 192"',
			'remindme "tomorrow at 10am"'
			'remindme "5pm"'
		]
	}
	async def cmd_remindme(self, message, args, kwargs):
		expiry = dateparser.parse(args[0], settings={'PREFER_DATES_FROM': 'future'})

		if expiry is None:
			await self.send_error(message, comment=f'couldn\'t understand your date or duration (\'{args[0]}\')')
			return

		duration = expiry - datetime.datetime.now()

		if duration < datetime.timedelta(0):
			await self.send_error(message, comment=f'can\'t set timer for {expiry} (datetime is in the past)')
			return

		await message.channel.send(f'<timer for {expiry}>')

	async def cmd_parse_date(self, message, args, kwargs):
		await message.channel.send(dateparser.parse(" ".join(args)) or "<:EnemyMissing:434620725891039242>")