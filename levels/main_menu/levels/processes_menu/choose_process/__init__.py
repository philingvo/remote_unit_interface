#coding: utf-8

from levels.basic_levels import Level_with_Downloading


class Choose_Process(Level_with_Downloading):

	name = "Choose Process"
	command = "switch_process"
	main_color = "blue"
	pathname = "working_processes_names"
	item_key = "name"
	downloading_target = "Working processes names"

	def get_command_dict(self):
		command_dict = self.interface.get_command_message(self.command)
		command_dict["process_name"] = self.response[self.item_position][self.item_key]
		return command_dict