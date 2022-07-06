#coding: utf-8

from levels.basic_levels import Level
from .change_letters_case_style import Change_Letters_Case_Style
from .change_auto_pronunciation import Change_Auto_Pronunciation


class Interface_Settings_Menu(Level):
	name = "Interface Settings"
	main_color = "crimson"
	items = [
			Change_Letters_Case_Style,
			Change_Auto_Pronunciation
			]