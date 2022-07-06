#coding: utf-8

from levels.basic_levels import Interface_Setting_Choosing_Level
from levels.basic_levels import Level


class Upper_Case(Level):
	name = "upper style"
	value = "upper"
	color = "red"

class Capitalize_Case(Level):
	name = "capitalize style"
	value = "capitalize"
	color = "pink"

class Title_Case(Level):
	name = "title style"
	value = "title"
	color = "orange"

class Lower_Case(Level):
	name = "lower style"
	value = "lower"
	color = "green"

class Original_Level_Name_Case(Level):
	name = "oRiginal level name case"
	value = None
	color = "gray"

class Change_Letters_Case_Style(Interface_Setting_Choosing_Level):
	name = "leter case style"
	main_color = "green"
	setting_name = "letters_case_style"
	check_value = True
	items = [
			Upper_Case,
			Capitalize_Case,
			Title_Case,
			Lower_Case,
			Original_Level_Name_Case
			]

	def change_setting_value(self, new_value):
		super().change_setting_value(new_value)
		self.show_item_title()

	def show_item_title(self):
		message = self.get_item_title_message()
		letter_case_method = self.item_class.value
		self.send_text_message(message, letter_case_method=letter_case_method)