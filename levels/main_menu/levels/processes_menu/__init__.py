#coding: utf-8

from levels.basic_levels import Level
from levels.basic_levels import Command
from .choose_process import Choose_Process


class Start_Process_Beginning(Command):

	name = "Start With Beginning"
	command = "process_beginning"
	main_color = "purple"

	def open(self):
		self.command = self.interface.get_command_message(self.command)
		self.command["process_name"] = self.previous_level.process_name
		super().open()

class Current_Standby_Process(Level):

	name = basic_name = "Current Standby Process"
	main_color = "orange"
	items = [
			Start_Process_Beginning
			]

	@classmethod
	def change_name(self, process_name):
		self.process_name = process_name
		self.name = "{} - {}".format(process_name.replace("_", " "), self.basic_name)

class Next_Process(Command):

	name = "Next Process"
	command = "next_process"
	main_color = "green"

class Previous_Process(Command):

	name = "Previous Process"
	command = "previous_process"
	main_color = "red"

class Processes_Menu(Level):

	name = "Working Processes"
	main_color = "green"
	items = [
			Current_Standby_Process,
			Next_Process,
			Previous_Process,
			Choose_Process
			]
	changeable_items = [
						Current_Standby_Process
						]