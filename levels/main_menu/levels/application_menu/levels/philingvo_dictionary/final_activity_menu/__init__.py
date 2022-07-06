#coding: utf-8

from levels.basic_levels import Level
from levels.main_menu.levels.interface_settings_menu import Interface_Settings_Menu


class Return_Item(Level):
	destination_level_class_name = None
	open_method_name = None
	
class Back_To_Mode_Info_Menu_Activity(Return_Item):
	name = "back"
	main_color = "orange"
	destination_level_class_name = "activity process"
	open_method_name = "reopen_activity_and_show_info_field_item"

class Back_To_Mode_Last_Step_Activity(Return_Item):
	name = "back to the activity last step"
	main_color = "orange"
	destination_level_class_name = "activity process"
	open_method_name = "reopen_activity_last_step"

class Repeat_Mode(Return_Item):
	name = "repeat with beginning"
	main_color = "green"
	destination_level_class_name = "activity process"
	open_method_name = "repeat"

class Choose_Another_Params(Return_Item):
	name = "choose another parameters"
	main_color = "green"
	destination_level_class_name = "parameters source"

class Choose_Another_Elements_Length(Return_Item):
	name = "choose another elements' length"
	main_color = "pink"
	destination_level_class_name = "choose elements length"

class Choose_Another_Mode(Return_Item):
	name = "choose another mode"
	main_color = "yellow"
	destination_level_class_name = "mode"

class Choose_Another_Preset(Return_Item):
	name = "choose another preset"
	main_color = "lime"
	destination_level_class_name = "preset"

class Back_To_Sets(Return_Item):
	name = "back to sets"
	main_color = "purple"
	destination_level_class_name = "sets"

class Back_To_Topics(Return_Item):
	name = "back to topics"
	main_color = "blue"
	destination_level_class_name = "topics"

class Back_To_Subjects(Return_Item):
	name = "back to subjects"
	main_color = "red"
	destination_level_class_name = "subjects"

class Back_To_Playlist_Set(Return_Item):
	name = "back to playlist's sets"
	main_color = "purple"
	destination_level_class_name = "sets in playlist"

class Back_To_Playlists(Return_Item):
	name = "back to playlists"
	main_color = "green"
	destination_level_class_name = "playlists"

class Back_To_Dictionaty_Menu(Return_Item):
	name = "back to dictionary menu"
	main_color = "blue"
	destination_level_class_name = "philingvo dictionary"

class Back_To_Main_Menu(Return_Item):
	name = "Back to Main Menu"	
	main_color = "red"
	destination_level_class_name = "main menu"

class Final_Activity_Menu(Level):
	name = "return activity menu"
	items = [
			Back_To_Mode_Info_Menu_Activity,
			Back_To_Mode_Last_Step_Activity,
			Repeat_Mode,
			Interface_Settings_Menu,
			Choose_Another_Params,
			Choose_Another_Elements_Length,
			Choose_Another_Mode,
			Choose_Another_Preset,
			Back_To_Sets,
			Back_To_Topics,
			Back_To_Subjects,
			Back_To_Playlist_Set,
			Back_To_Playlists,
			Back_To_Dictionaty_Menu,
			Back_To_Main_Menu
			]
	back_to_mode_class = Back_To_Mode_Info_Menu_Activity

	no_level_in_previous_levels_text = "Can't find level"

	def __init__(self, previous_level):
		super().__init__(previous_level)
		self.create_previous_levels_dict()

	def create_previous_levels_dict(self):
		self.previous_levels_dict = {}
		level = self
		while isinstance(level, Level):
			self.previous_levels_dict[level.name.lower()] = level
			level = level.previous_level

	def open(self, **kwargs):
		super().open()
		self.copy_input_params(kwargs)

	def show_first_item(self):
		self.item_position = 0
		if len(self.items) > 0:
			self.find_level(self.down)

	def copy_input_params(self, kwargs):
		self.params = kwargs

	def is_return_level(self, item_class):
		return issubclass(item_class, Return_Item)

	def is_level_in_previous_levels(self, item_class):
		return self.is_return_level(item_class) and item_class.destination_level_class_name in self.previous_levels_dict	

	def open_level(self, item_class):
		if self.is_level_in_previous_levels(item_class):
			level = self.previous_levels_dict[item_class.destination_level_class_name]
			if item_class.open_method_name:
				level.__getattribute__(item_class.open_method_name)()
			else:
				level.comeback()
		elif not self.is_return_level(item_class):
			item = item_class(self)
			item.open()
		else:
			self.send_error_message(self.no_level_in_previous_levels_text)

	def activate(self):
		if len(self.items) > 0:
			self.item_class = self.get_item_class()
			self.open_level(self.item_class)

	@staticmethod
	def is_property_in_class(item_class, property_name):
		return property_name in item_class.__dict__

	def show_item_title(self, item_class=False):
		super().show_item_title()
		if item_class:
			item_class = self.item_class
		self.assign_item_language_for_pronunciation(item_class)

	def find_level(self, method):

		item_class = self.get_item_class()
		if self.is_level_in_previous_levels(item_class):
			self.show_item_title(item_class)
		elif not self.is_return_level(item_class) and self.is_property_in_class(item_class, "name"):
			self.show_item_title(item_class)
		else:
			method()

	def up(self):
		self.item_position -= 1
		if self.item_position < 0:
			self.item_position = len(self.items) - 1
		self.find_level(self.up)

	def down(self):
		self.item_position += 1
		if self.item_position >= len(self.items):
			self.item_position = 0
		self.find_level(self.down)

	def back(self):
		if self.back_to_mode_class:
			self.open_level(self.back_to_mode_class)