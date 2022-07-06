#coding: utf-8

from levels.basic_levels import Level
from .levels.application_menu import Application_Menu
from .levels.control_menu import Control_Menu
from .levels.processes_menu import Processes_Menu
from .levels.messages_menu import Messages_Menu
from .levels.interface_settings_menu import Interface_Settings_Menu


class Main_Menu(Level):

	name = "main menu"
	items = [
			Application_Menu,
			Control_Menu,
			Processes_Menu,
			Messages_Menu,
			Interface_Settings_Menu
			]