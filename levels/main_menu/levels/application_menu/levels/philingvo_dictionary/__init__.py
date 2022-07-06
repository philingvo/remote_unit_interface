#coding: utf-8

from levels.basic_levels import Level
from .dictionary_navigation import Subjects
from .dictionary_navigation import Playlists


class Philingvo_Dictionary(Level):

	name = "Philingvo Dictionary"
	main_color = "blue"
	items = [
			Playlists,
			Subjects,
			]