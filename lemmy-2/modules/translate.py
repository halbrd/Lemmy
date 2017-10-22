from module import Module
import googletrans

class Translate(Module):
	info = 'Translates text to English'

	cmd_translate_usage = [
		'translate <expression>',
		'translate destination=<language> <expression>'
	]
	async def cmd_translate(self, message, args):
		if not args:
			return 'usage'

		destination = 'english'

		destination_prefix = 'destination='
		if args[0].startswith(destination_prefix):
			if len(args) == 1:   # there isn't an expression to translate
				raise Module.CommandError

			destination = args[0][len(destination_prefix):].lower()

			del args[0]

		reverse_language_lookup = { v: k for k, v in googletrans.LANGUAGES.items() }

		if not destination in reverse_language_lookup:
			raise Module.CommandError

		destination = reverse_language_lookup[destination]

		expression = ' '.join(args)
		translator = googletrans.Translator()
		translation = translator.translate(expression, dest=destination)
		await self.client.send_message(message.channel, translation.text)

	cmd_translate_languages_usage = [ 'translate_languages' ]
	async def cmd_translate_languages(self, message, args):
		await self.client.send_message(message.channel, ', '.join([ v for k, v in googletrans.LANGUAGES.items() ]))