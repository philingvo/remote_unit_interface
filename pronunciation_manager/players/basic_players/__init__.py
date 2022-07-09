#coding: utf-8

import os
from threading import Thread
from time import sleep
import functools


class Player_Basic:

	settings = None
	source_class = None

	def __init__(self, pronunciation_manager):
		self.collect_player_all_additional_settings()
		self.assign_additional_settings(pronunciation_manager)
		self.source = self.source_class(self)

	@classmethod
	def collect_player_all_additional_settings(self):

		def is_player_settings_in_class_ancestor(class_ancestor):
			return "settings" in class_ancestor.__dict__ and isinstance(getattr(class_ancestor, "settings"), dict)

		settings = {}
		for completed_player_class in [self, self.source_class]:
			classes_ancestors = completed_player_class.mro()
			for class_ancestor in classes_ancestors:
				if is_player_settings_in_class_ancestor(class_ancestor):
					settings.update(class_ancestor.settings)

		if len(settings) > 0:
			self.settings = settings

	def assign_additional_settings(self, pronunciation_manager):
		additional_player_settings = pronunciation_manager.additional_player_settings
		if isinstance(self.settings, dict):
			for user_named_property, class_attribute_name in self.settings.items():
				if additional_player_settings:
					setting_value = additional_player_settings[user_named_property]
				else:
					setting_value = class_attribute_name[1]
				setting_name = class_attribute_name[0]
				self.__setattr__(setting_name, setting_value)

class Saving_Pronunciation_File(Player_Basic):

	pronunciations_files_dir = "pronunciations"
	default_delete_audio_file_after = False # Deleting works for pygame version > 2
	delete_audio_file_after = None
	settings = {"delete_audio_file_after": ["default_delete_audio_file_after", False],
				"pronunciations_files_dir": ["pronunciations_files_dir", "pronunciations"]}

	filename_len_max = 50

	@staticmethod
	def check_path(path):
		return os.path.exists(path)

	@classmethod
	def check_path_existance(self, path):
		if not self.check_path(path):
			os.mkdir(path)
	
	def get_filepath_for_saving(self, text, lang):
		self.check_path_existance(self.pronunciations_files_dir)
		filepath = os.path.join(self.pronunciations_files_dir, lang)
		self.check_path_existance(filepath)

		if len(text) > self.filename_len_max:
			text = "{}...".format(text[:self.filename_len_max])

		filename = self.source.prepare_text("{} {}.mp3".format(lang, text).lower(), False)
		filepath = os.path.join(filepath, filename)
		return filepath
	
	def pronunciation_file_exists(saving_method):

		@functools.wraps(saving_method)
		def wrapper(self, **kwargs):
			filepath = self.get_filepath_for_saving(kwargs["text"], kwargs["lang"])
			if self.check_path(filepath) or self.check_path(filepath) and self.default_delete_audio_file_after:
				self.delete_audio_file_after = False
			else:
				saving_method(self, filepath, **kwargs)
				self.delete_audio_file_after = self.default_delete_audio_file_after
			return filepath

		return wrapper

	def finish_playing(self):
		if self.delete_audio_file_after:
			delete_after_playing_thread = Thread(target=self.delete_audio_file, args=[self.to_play])
			delete_after_playing_thread.start()

	def delete_audio_file(self, audio_file_path):
		while self.pg.mixer.music.get_busy():
			sleep(1)
		else:
			# self.pg.mixer.music.unload()
			os.remove(audio_file_path)
