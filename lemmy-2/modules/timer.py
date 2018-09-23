import sys
sys.path.append('..')
from module import Module

import datetime
import asyncio

class Timer(Module):
	docs = {
		'description': 'Posts an alert after a specified time period'
	}

	def __init__(self, lemmy):
		Module.__init__(self, lemmy)

        self.timers = self.load_data('timers', default='[]')

        for timer in self.timers:
            timer['creator'] = self.client.get_user(timer['creator'])
            timer['created'] = datetime.strptime(timer['created'], '%Y-%m-%d %H:%M%S')
            timer['expiration'] = datetime.strptime(timer['expiration'], '%Y-%m-%d %H:%M%S')
            timer['destination'] = self.client.get_channel(timer['destination'])

        asyncio.get_event_loop().create_task(self.check_timers())

timers = [
    {
        "creator": 123469284359287345,
        "expiration": "yyyy-MM-dd hh:mm:ss",
        "duration": "1d 2h 3m 4s"
        "message": "a something yes",
        "destination": 237462098173468765   # use client.get_channel(id)
    }
]

    async def check_timers(self):
        CHECK_INTERVAL = 1

        while True:
            # try:
            for timer in self.timers:
                if datetime.datetime.now() > timer['expiration']:
                    message = f'{timer["creator"].mention} Your timer for {timer["duration"]} is up.'
                    if timer['message']:
                        message += '\n' + timer['message']
                    await timer['destination'].send(message)

            await asyncio.sleep(CHECK_INTERVAL)
            # except Exception as e:   # prevent an exception from killing the job
            #     logging.error(f'Exception in check_timers job: {type(exception).__name__}: {str(exception)}')
            #     continue


	docs_timer = {
		'description': 'Starts a countdown timer',
		'usage': 'timer <duration> <message>',
		'examples': [ 'timer 3s', 'timer 1d2h3m4s', 'timer 7:45' ]
	}
	async def cmd_timer(self, message, args, kwargs):
		pass

    docs_remindme = {
        'description': 'Reminds the user of something at the specified time',
        'usage': 'remindme <activation date time> <message>',
        'examples': [ 'remindme 2020-09-24 "September 24th, 2020!"', 'remindme 2020-05-13/13:22:57 "1:22:57pm, May 13th, 2020!"' ]
    }
    async def cmd_remindme(self, message, args, kwargs):
        pass
