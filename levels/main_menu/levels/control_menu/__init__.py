#coding: utf-8

from levels.basic_levels import Level
from levels.basic_levels import Command
from .speed_control import Speed_Control_Menu


class Pause_Resume_Command(Command):
	name = "Pause/Resume"
	main_color = "blue"	
	command = "pause"

class Stop_Command(Command):
	name = "Stop"
	main_color = "red"
	command = "stop"

class Wait_Command(Command):
	name = "Wait"
	main_color = "purple"
	command = "wait"

class Off_Command(Command):
	name = "Off"
	main_color = "crimson"
	command = "off"

class On_Command(Command):
	name = "On"
	main_color = "green"
	command = "on"

class Standby_Command(Command):
	name = "Standby"
	main_color = "lime"
	command = "standby"

class Date_Time_Command(Command):
	name = "Show Date and Time"
	main_color = "orange"
	command = "date_time"

class Control_Menu(Level):
	name = "Control Commands"
	main_color = "purple"
	items = [
			Pause_Resume_Command,
			Stop_Command,
			Wait_Command,
			Off_Command,
			On_Command,
			Standby_Command,
			Date_Time_Command,
			Speed_Control_Menu
			]