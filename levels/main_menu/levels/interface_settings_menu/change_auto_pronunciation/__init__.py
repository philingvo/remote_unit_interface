#coding: utf-8

from levels.basic_levels import Interface_Setting_Choosing_Level
from levels.basic_levels import Yes
from levels.basic_levels import No


class Yes(Yes):
	value = True

class No(No):
	value = False

class Change_Auto_Pronunciation(Interface_Setting_Choosing_Level):
	name = "Auto Pronunciation"
	main_color = "blue"
	setting_name = "auto_pronunciation"
	items = [
			Yes,
			No
			]