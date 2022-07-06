#coding: utf-8

from levels.basic_levels import Level
from .levels.philingvo_dictionary import Philingvo_Dictionary


class Application_Menu(Level):

	name = "applications"
	items = [
			Philingvo_Dictionary
			]