#coding: utf-8

from levels.basic_levels import Level


class Axilary_Part_Info_Level(Level):

	def open(self, language_for_pronunciaition):
		self.set_level()
		self.assign_language_for_pronunciation(language_for_pronunciaition)

	def up(self):
		self.back()
		self.previous_level.up()

	def down(self):
		self.back()
		self.previous_level.down()

	def left(self):
		self.back()

	def right(self):
		self.back()

	def activate(self):
		self.back()

class Part_Info_Menu_Level(Level):

	name = "part information menu"
	use_auxilary_level = True
	
	def show_menu_title(self):
		menu_title_message = self.__class__.get_colored_title(self.interface)
		self.send_text_message(menu_title_message)

	def back(self):
		self.previous_level.reopen_and_show_info_field_item()

	def get_item_title(self):
		self.item_class = self.get_item_class()
		return self.item_class

	def activate(self):
		if self.item_class:
			self.previous_level.run_show_method(self.item_class, True)
			auxilary_level = Axilary_Part_Info_Level(self)
			auxilary_level.open(self.previous_level.language_for_pronunciaition)
			# self.previous_level.assign_language_for_pronunciation(self.previous_level.language)
			self.previous_level.assign_level_language_for_pronunciation()

	def open_single_item(self):
		self.previous_level.run_show_method(self.item_class, False)

	def open_and_show_no_items_message(self):
		self.set_level()
		message = self.get_no_items_error_message()
		self.send_text_message(message)

	def open(self):
		items_length = len(self.items)
		if items_length == 0:
			self.open_and_show_no_items_message()
		elif items_length == 1:
			self.get_item_title()
			self.open_single_item()
		else:
			super().open()

class Activity_Menu(Part_Info_Menu_Level):
	name = "activity menu"
	main_color = "green"
	items = ["final activity menu"]
	use_auxilary_level = False

class Part_Info_Menu(Part_Info_Menu_Level):
	name = "part information"
	main_color = "orange"
	items = ["part position",
			"part name",
			"part format",
			"part language"]

class Set_Info_Menu(Part_Info_Menu_Level):
	name = "set information"
	main_color = "purple"
	items = ["set title",
			"set type",
			"set language",
			"set abstract",
			"set ID",
			"topic title",
			"subject title",
			"playlist title"]

class Slice_Info_Menu(Part_Info_Menu_Level):
	name = "slice information"
	main_color = "blue"
	items = ["element position",
			"slice position",
			"slice title",
			"mode name",
			"activity name",
			"elements order",
			"parts order"]