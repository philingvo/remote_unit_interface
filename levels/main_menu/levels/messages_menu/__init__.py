#coding: utf-8

from levels.basic_levels import Level
from levels.basic_levels import Command
from levels.basic_levels import Basic_Change_Status_Command
from ..control_menu import Stop_Command
from .repeat_message_statuses import Repeat_Message_Statuses_Command


class Next_Message_Command(Command):
	name = "Next Message"
	main_color = "green"
	command = "next_message"

class Previous_Message_Command(Command):
	name = "Previous Message"
	main_color = "red"
	command = "previous_message"

class Next_Received_Message_Command(Command):
	name = "Next Received Message"
	main_color = "purple"
	command = "next_received_message"

class Previous_Received_Message_Command(Command):
	name = "Previous Received Message"
	main_color = "orange"
	command = "previous_received_message"

class Change_Refresh_Message_Status_Command(Basic_Change_Status_Command):
	name_template = name = "Turn {} Refresh Message Status"
	main_color = "orange"
	command = "change_refresh_message_status"

class Change_Deny_Receiving_Status(Basic_Change_Status_Command):
	name_template = name = "Turn {} Deny Receiving Status"
	main_color = "purple"
	command = "change_deny_receiving_status"

class Messages_Menu(Level):
	name = "messages control"
	main_color = "blue"
	items = [
	Next_Message_Command,
			Previous_Message_Command,
			Next_Received_Message_Command,
			Previous_Received_Message_Command,
			Repeat_Message_Statuses_Command,
			Change_Refresh_Message_Status_Command,
			Change_Deny_Receiving_Status
			]
	changeable_items = [
						Change_Refresh_Message_Status_Command,
						Change_Deny_Receiving_Status
						]