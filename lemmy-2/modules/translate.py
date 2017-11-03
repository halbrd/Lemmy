from module import Module
import googletrans

class Translate(Module):
	docs = {
		'description': 'Translates text between languages using Google Translate'
	}

	docs_translate = {
		'description': 'Translates text between languages',
		'usage': 'translate <source=language> <destination=language> phrase',
		'examples': [ 'translate Kartoffel', 'translate source=de pommes', 'translate destination=korean bong bong' ]
	}
	async def cmd_translate(self, message, args, kwargs):
		if not args:
			raise Module.CommandError

		source = kwargs['source'].lower() if 'source' in kwargs else None
		destination = kwargs['destination'].lower() if 'destination' in kwargs else 'english'

		if source is not None and source not in googletrans.LANGUAGES and source not in googletrans.LANGCODES:
			raise Module.CommandError

		if destination not in googletrans.LANGUAGES and destination not in googletrans.LANGCODES:
			raise Module.CommandError

		if source is not None:
			source = googletrans.LANGUAGES[source] if source in googletrans.LANGUAGES else googletrans.LANGCODES[source]
		destination = googletrans.LANGUAGES[destination] if destination in googletrans.LANGUAGES else googletrans.LANGCODES[destination]

		expression = ' '.join(args)
		translator = googletrans.Translator()
		if source is None:
			translation = translator.translate(expression, dest=destination)
		else:
			translation = translator.translate(expression, src=source, dest=destination)
		await self.client.send_message(message.channel, f'{translation.origin} `[{googletrans.LANGUAGES[translation.src.lower()].title()}] => [{googletrans.LANGUAGES[translation.dest.lower()].title()}]` {translation.text}')

	docs_translate_languages = {
		'description': 'Lists available languages and codes'
	}
	async def cmd_translate_languages(self, message, args, kwargs):
		await self.client.send_message(message.channel, ', '.join([ f'{v.title()} `[{k}]`' for k, v in googletrans.LANGUAGES.items() ]))
