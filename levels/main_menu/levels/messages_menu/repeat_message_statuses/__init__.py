#coding: utf-8

from levels.basic_levels import Level
from levels.basic_levels import Basic_Change_Status_Command


class Basic_Change_Repeat_Message_Status_Command(Basic_Change_Status_Command):
	name_template = "Turn {} for {} process"
	command = "change_repeat_message_status"
	name = process_name = False

	@classmethod
	def change_name(self, status):
		self.status = status
		self.name = self.name_template.format(self.get_command_text(),
											self.process_name.replace("_", " "))
		self.fill_letters_colors()

	def open(self):
		self.command = self.interface.get_command_message(self.command)
		self.command["process_name"] = self.process_name
		super().open()

class Change_Repeat_Message_Status_For_Message_Process_Command(Basic_Change_Repeat_Message_Status_Command):
	process_name = "message"
	main_color = "orange"

class Change_Repeat_Message_Status_For_Standby_Process_Command(Basic_Change_Repeat_Message_Status_Command):
	process_name = "standby"
	main_color = "yellow"

class Repeat_Message_Statuses_Command(Level):
	name = "Repeat Message"
	main_color = "yellow"
	items = [
			Change_Repeat_Message_Status_For_Message_Process_Command,
			Change_Repeat_Message_Status_For_Standby_Process_Command
			]
	changeable_items = [
						Change_Repeat_Message_Status_For_Message_Process_Command,
						Change_Repeat_Message_Status_For_Standby_Process_Command
						]