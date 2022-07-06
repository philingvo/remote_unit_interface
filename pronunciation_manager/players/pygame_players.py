#coding: utf-8

import requests
import urllib.request as request
import json

from .basic_players import Player_Basic
from .basic_players import Saving_Pronunciation_File

from .sources import Philingvo_Dictionary_Source_Audio
from .sources import Philingvo_Dictionary_Source_Local_Filepath
from .sources import gTTS_Source_Stream
from .sources import gTTS_Source_Basic


class Pygame_Player_Basic(Player_Basic):

	def __init__(self, pronunciation_manager):
		super().__init__(pronunciation_manager)
		self.pg = pronunciation_manager.pg
		self.pg.mixer.init()

	def __call__(self, **kwargs):
		self.to_play = self.load_audio(**kwargs)
		if self.to_play:
			self.play()

	def play(self):
		self.pg.mixer.music.play()

	def pause(self):
		if self.pg.mixer.music.get_busy():
			self.pg.mixer.music.pause()
		else:
			self.pg.mixer.music.unpause()

	def load_audio(self, loading_object):
		try:
			self.pg.mixer.music.load(loading_object)
			return loading_object
		except Exception as loading_error:
			print(loading_error)
			return False

class Pygame_Philingvo_Dictionary_Audio_Basic(Pygame_Player_Basic):

	def load_audio(self, **kwargs):
		request_url = self.source.get_request_url(**kwargs)
		if request_url:
			try:
				response_to_load = self.get_response(request_url, **kwargs)
				if not response_to_load:
					raise Exception(self.source.request_error_message_text)
			except Exception as request_error:
				return self.source.output_server_message_error(request_error)
			else:
				super().load_audio(response_to_load)
				return response_to_load
		else:
			return self.source.output_server_message_error(self.source.create_request_url_error_message_text)

	def get_response(self, request_url, **kwargs):
		return False

	def check_response(make_request_method):

		def check_status(response):
			status_names = ["status_code" , "status"]
			for status_name in status_names:
				if status_name in response.__dict__ and response.__getattribute__(status_name) == 200:
					return True

		def wrapper(self, *args, **kwargs):
			response = make_request_method(self, *args, **kwargs)
			if check_status(response):
				return response
			else:
				return False

		return wrapper

class Pygame_gTTS_Player_Basic(Pygame_Player_Basic):

	def load_audio(self, **kwargs):
		try:
			object_to_load = self.load_audio_from_source(**kwargs)
			return super().load_audio(object_to_load)
		except Exception as request_error:
			return self.source.output_server_message_error(request_error)

class Pygame_Philingvo_Dictionary_Audio_Stream(Pygame_Philingvo_Dictionary_Audio_Basic):
	# Streaming works for python 3.7.9 and pygame 1.9.4
	source_class = Philingvo_Dictionary_Source_Audio

	@Pygame_Philingvo_Dictionary_Audio_Basic.check_response
	def get_response(self, request_url, **kwargs):
		return requests.get(request_url, stream=True).raw

class Pygame_Philingvo_Dictionary_Audio_Saving(Pygame_Philingvo_Dictionary_Audio_Basic, Saving_Pronunciation_File):

	source_class = Philingvo_Dictionary_Source_Audio
	settings = {"delete_audio_file_after": ["default_delete_audio_file_after", True]}

	def get_response(self, request_url, **kwargs):
		return self.make_request_and_save(request_url=request_url, **kwargs)

	@Saving_Pronunciation_File.pronunciation_file_exists
	def make_request_and_save(self, filepath, **kwargs):
		request_url = kwargs["request_url"]
		try:
			request.urlretrieve(request_url, filepath)
		except Exception as request_error:
			return self.source.output_server_message_error(request_error)

	def play(self, **kwargs):
		super().play(**kwargs)
		self.finish_playing()

class Pygame_Philingvo_Dictionary_Local_Filepath(Pygame_Philingvo_Dictionary_Audio_Basic):

	source_class = Philingvo_Dictionary_Source_Local_Filepath
	filepath_key = "local_filepath"

	@Pygame_Philingvo_Dictionary_Audio_Basic.check_response
	def make_request(self, request_url):
		return requests.get(request_url)

	def get_response(self, request_url, **kwargs):
		response = self.make_request(request_url)
		if response:
			path = json.loads(response.text)[self.filepath_key]
			return path
		else:
			return False

class Pygame_gTTS_Stream_Player(Pygame_gTTS_Player_Basic):
	# Doesn't work
	source_class = gTTS_Source_Stream

	def load_audio_from_source(self, text, lang):
		return self.source.get_audio(text, lang)

class Pygame_gTTS_Saving_Player(Pygame_gTTS_Player_Basic, Saving_Pronunciation_File):

	source_class = gTTS_Source_Basic
	settings = {"delete_audio_file_after": ["default_delete_audio_file_after", False]}

	def load_audio_from_source(self, **kwargs):
		return self.download(**kwargs)

	@Saving_Pronunciation_File.pronunciation_file_exists
	def download(self, filepath, text, lang):
		audio = self.source.get_audio(text, lang)
		audio.save(filepath)

	def play(self, **kwargs):
		super().play(**kwargs)
		self.finish_playing()