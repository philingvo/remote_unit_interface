#coding: utf-8

from .players.pygame_players import Pygame_gTTS_Stream_Player
from .players.pygame_players import Pygame_gTTS_Saving_Player
from .players.pygame_players import Pygame_Philingvo_Dictionary_Audio_Stream
from .players.pygame_players import Pygame_Philingvo_Dictionary_Audio_Saving
from .players.pygame_players import Pygame_Philingvo_Dictionary_Local_Filepath
from .players.vlc_players import VLC_Philingvo_Dictionary_Audio_Player
from .players.vlc_players import VLC_Philingvo_Dictionary_Audio_With_Ballast_Player


class Pronunciation_Manager:

	user_settings_names = [
						"language",
						"pronunciation_player_name",
						"play_random_pronunciation_file",
						"additional_player_settings",
						]

	language = "en"
	pronunciation_player_name = "gtts_saving"
	additional_player_settings = None
	
	pronunciation_players = {
							"gtts_stream": Pygame_gTTS_Stream_Player,
							"gtts_saving": Pygame_gTTS_Saving_Player,
							"pygame_philingvo_dictionary_audio_stream": Pygame_Philingvo_Dictionary_Audio_Stream,
							"pygame_philingvo_dictionary_audio_saving": Pygame_Philingvo_Dictionary_Audio_Saving,
							"pygame_philingvo_dictionary_local_filepath": Pygame_Philingvo_Dictionary_Local_Filepath,
							"vlc_philingvo_dictionary_stream": VLC_Philingvo_Dictionary_Audio_Player,
							"vlc_philingvo_dictionary_stream_with_ballast": VLC_Philingvo_Dictionary_Audio_With_Ballast_Player,
							}
	pronunciation_player = None
	empty_text = "No text to pronounce"

	def __init__(self, user_settings=False, pygame=False):
		self.user_settings = user_settings
		self.assign_user_settings()
		self.import_pygame(pygame)
		self.create_pronunciation_player()

	def import_pygame(self, pygame):
		if pygame:
			self.pg = pygame
		else:
			import pygame as pg
			self.pg = pg

	def assign_user_settings(self):
		if isinstance(self.user_settings, dict):
			for setting_name in self.user_settings_names:
				self.assign_setting(setting_name)

	def assign_setting(self, setting_name):
		if setting_name in self.__class__.__dict__:
			setting_value = self.user_settings.get(setting_name)
			if setting_value:
				self.__setattr__(setting_name, setting_value)

	def create_pronunciation_player(self):
		pronunciation_player_class = self.pronunciation_players.get(self.pronunciation_player_name)
		if pronunciation_player_class:
			self.pronunciation_player = pronunciation_player_class(self)

	def pronounce(self, text=False, lang=False):
		if not text:
			text = self.empty_text
		lang = lang.lower() if lang else self.language
		if self.pronunciation_player:
			self.pronunciation_player(text=text, lang=lang)

	def pronunciation_pause(self):
		if self.pronunciation_player:
			self.pronunciation_player.pause()