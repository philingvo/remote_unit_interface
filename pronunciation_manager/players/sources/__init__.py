#coding: utf-8

import re
from urllib.parse import quote


class Source_Basic:

	server_error_message_text_basic = "Can't connect to"
	name = "Pronunciation Source"
	create_request_url_error_message_text = "Request url can't be create"
	request_error_message_text = "Request can't be inplemented"

	def __init__(self, *args, **kwargs):
		pass

	@staticmethod
	def prepare_text(text, prepare_for_url=True):
		prepared_text = re.sub("[/\\:*«<>|#&\n\r\t]", " ", text)
		if prepare_for_url:
			prepared_text = prepared_text.replace("?", ' ')
			prepared_text = quote(prepared_text)
		else: # for file
			prepared_text.replace("?", '؟')
		return prepared_text

	@classmethod
	def output_server_message_error(self, request_error):
		print("{} {}: {}".format(self.server_error_message_text_basic, self.name, request_error))
		return False

class Philingvo_Dictionary_Source_Basic(Source_Basic):

	name = "Philingvo Dictionary"
	url_template = "http://{}/{}/?lang={}&text={}"
	server_route = None
	philingvo_dictionary_pronunciation_server_address = None
	settings = {"philingvo_dictionary_pronunciation_server_address": ["philingvo_dictionary_pronunciation_server_address", None],
				"play_random_pronunciation_file": ["play_random_pronunciation_file", None]}

	def __init__(self, player):
		self.philingvo_dictionary_pronunciation_server_address = player.philingvo_dictionary_pronunciation_server_address
		self.play_random_pronunciation_file = player.play_random_pronunciation_file

	def get_request_url(self, text, lang):
		if self.philingvo_dictionary_pronunciation_server_address and self.server_route and text and lang:
			url = self.url_template.format(self.philingvo_dictionary_pronunciation_server_address,
											self.server_route,
											self.prepare_text(lang),
											self.prepare_text(text))
			if self.play_random_pronunciation_file:
				url = "{}&random=t".format(url)
			return url
		else:
			return False

class Philingvo_Dictionary_Source_Audio(Philingvo_Dictionary_Source_Basic):
	server_route = "pronounce"
	
class Philingvo_Dictionary_Source_Local_Filepath(Philingvo_Dictionary_Source_Basic):
	server_route = "pronunciation_local_filepath"

from gtts import gTTS
class gTTS_Source_Basic(Source_Basic):
	name = "gTTS"

	def get_audio(self, text, lang):
		return gTTS(text=text, lang=lang)

from io import BytesIO
class gTTS_Source_Stream(gTTS_Source_Basic):

	def get_audio(self, text, lang):
		tts = super().get_audio(text, lang)
		fp = BytesIO()
		tts.write_to_fp(fp)
		fp.seek(0)
		return fp