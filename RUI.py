#!/usr/bin/python3
#coding: utf-8

from urllib import request
import sys
import json
import pygame as pg
import http
import requests
from user_settings import user_settings
from color_codes import color_codes
from levels.main_menu import Main_Menu
from pronunciation_manager import Pronunciation_Manager


class User_Interface():

	test_mode = False
	start_available = None

	user_settings_names = ["test_mode",
							"led_server_address",
							"led_server_address_port",
							"language",
							"auto_pronunciation",
							"pronunciation_settings",
							"application_settings",
							"window_settings",
							"letters_case_style",
							"keys"]

	led_server_address = None
	led_server_address_port = None

	language = "en"
	auto_pronunciation = False

	pronunciation_settings = None
	application_settings = None
	
	window_settings = None
	window_width = 400
	window_height = 300
	window_background_color = "black"
	window_text_color = "red"
	window_font_height = 36

	letters_case_style = None
	possible_letters_case_style = ["upper", "capitalize", "title", "lower"]
	
	keys = {"open": "home",
			"up": "up",
			"down": "down",
			"left": "left",
			"right": "right",
			"main_menu": "home",
			"back": "backspace",
			"repeat_sending": "f_5",
			"pronounce": "space",
			"quit": "escape",
			}

	zero_level = None
	level = None
	pronunciation_manager = None

	check_message_text = "Control Interface Connecting"
	check_message_color = "purple"
	check_failed_message_text = "Can't find the LED-server"
	start_message_text = "Control interface app is connected"
	start_message_color = "blue"
	request_error_message_text = "Can't send a message to LED-server"
	wrong_command_text = "Wrong command"

	zero_level_class = Main_Menu
	color_codes = color_codes
	user_settings = user_settings
	changeable_items_names = {
							# "Change_Repeat_Message_Status_Command": "repeat_message_status",
							"Change_Repeat_Message_Status_For_Message_Process_Command": "repeat_message_status_message",
							"Change_Repeat_Message_Status_For_Standby_Process_Command": "repeat_message_status_standby",
							# "Change_Repeat_Message_Status_For_Message_Store_Process_Command": "repeat_message_status_message_store",
							"Change_Refresh_Message_Status_Command": "refresh_message_status",
							"Change_Deny_Receiving_Status": "deny_receiving_status",
							"Current_Standby_Process": "standby_working_process_name",
							"Set_Delay_Time": "scrolling_delay_time"}

	levels_changeable_names_pathlists = {"repeat_message_status": ("Messages_Menu", "Change_Repeat_Message_Status_Command"),
										"refresh_message_status": ("Messages_Menu", "Change_Refresh_Message_Status_Command"),
										"deny_receiving_status": ("Messages_Menu", "Change_Deny_Receiving_Status"),
										"standby_working_process_name": ("Processes_Menu", "Current_Standby_Process")}

	last_text_message = None

	def __init__(self,):
		self.assign_user_settings()
		self.assign_window_settings()
		self.open_window()
		self.create_full_led_server_address()
		self.run_pronunciation_manager()
		self.assign_keys()
		self.check_server_connection_and_start()
		self.listen_to_keys()

	def assign_user_settings(self):
		if isinstance(self.user_settings, dict):
			for setting_name in self.user_settings_names:
				self.assign_setting(setting_name)

	def assign_setting(self, setting_name):
		if setting_name in self.__class__.__dict__:
			setting_value = self.user_settings.get(setting_name)
			if setting_value:
				self.__setattr__(setting_name, setting_value)

	def assign_window_settings(self):
		if "width" in self.window_settings:
			self.window_width = self.window_settings["width"]
		if "height" in self.window_settings:
			self.window_height = self.window_settings["height"]
		if "background_color" in self.window_settings:
			self.window_background_color = self.window_settings["background_color"]
		if "text_color" in self.window_settings:
			self.window_text_color = self.window_settings["text_color"]
		if "font_height" in self.window_settings:
			self.window_font_height = self.window_settings["font_height"]

	def open_window(self):
		self.display = pg.display.set_mode((self.window_width, self.window_height))
		pg.font.init()

	def run_pronunciation_manager(self):
		if self.pronunciation_settings and "pronunciation_player_name" in self.pronunciation_settings:
			self.pronunciation_settings["language"] = self.language
			self.pronunciation_manager = Pronunciation_Manager(self.pronunciation_settings, pg)

	def assign_keys(self):
		for action_name, raw_key in self.keys.items():
			if isinstance(raw_key, str):
				raw_key = raw_key.upper()
			elif isinstance(raw_key, tuple):
				raw_key = raw_key[0]
			self.keys[action_name] = getattr(pg, "K_{}".format(raw_key))

	def get_key(self, action_name):
		return self.keys[action_name]

	def check_server_connection_and_start(self):
		result = self.check_connection_to_led_server()
		self.start() if result else self.stop_starting()

	def create_full_led_server_address(self):
		self.full_led_server_address = 'http://{}:{}'.format(self.led_server_address, self.led_server_address_port)

	def check_connection_to_led_server(self):
		check_message = self.get_colored_text_message(self.check_message_text, main_color=self.check_message_color)
		return self.send_text_message(check_message, pronounce=False)

	def start(self):
		self.start_available = True
		self.send_start_message()
		self.set_and_open_zero_level()

	def send_start_message(self):
		start_message = self.get_colored_text_message(self.start_message_text, main_color=self.start_message_color)		
		self.send_text_message(start_message)

	def set_and_open_zero_level(self):
		self.zero_level = self.level = self.zero_level_class(self)
		self.zero_level.open()

	def stop_starting(self):
		self.start_available = False
		fail_message_text = self.get_error_message(self.check_failed_message_text)
		self.create_text_message_and_output_to_interface_window(fail_message_text)

	def change_letters_case(self, text, style_method_name):
		
		def is_style_method_possible(style_method_name):
			return isinstance(style_method_name, str) and style_method_name.lower() in self.possible_letters_case_style

		if style_method_name:
			if is_style_method_possible(style_method_name):
				style_method_name = style_method_name
			elif is_style_method_possible(self.letters_case_style):
				style_method_name = self.letters_case_style
			else:
				return text
			style_method = getattr(str, style_method_name.lower())
			return style_method(str(text))
		else:
			return text

	def create_text_message_and_output_to_interface_window(self, message):
		self.create_text_message_data(message)
		self.output_to_interface_window()

	def send_text_message(self, message, letter_case_method=True, pronounce=True):
		self.create_text_message_data(message, letter_case_method)
		if self.auto_pronunciation and pronounce:
			if self.level:
				lang = self.level.language_for_pronunciaition
			else:
				lang = None
			self.pronounce(self.last_text_message["string"], lang)
		return self.send()

	def send_error_message(self, error_text):
		message = self.get_error_message(error_text)
		self.send_text_message(message, letter_case_method="upper")

	def create_text_message_data(self, message, letter_case_method=False):
		if isinstance(message, dict) and "string" in message:
			message_dict = message
		else:
			message_dict = self.get_text_message(message)

		self.last_text_message = message_dict
		self.last_letter_case_method = letter_case_method

		if letter_case_method:
			message_dict["string"] = self.change_letters_case(message_dict["string"], letter_case_method)
		
		self.internal_message_dict = message_dict
		self.create_post_data(message_dict)

	def send_command(self, command_message):
		if isinstance(command_message, dict) and "command" in command_message:
			message_dict = command_message
			
			self.internal_message_dict = {"string": command_message["command"]}
		elif isinstance(command_message, str):
			message_dict = self.get_command_message(command_message)
			self.internal_message_dict = {"string": command_message}
		else:
			message_dict = False
			self.internal_message_dict = {"string": self.wrong_command_text}
		
		if message_dict:
			self.create_post_data(message_dict)
			show_in_interface_window = self.user_settings.get("show_command_messages_in_window", True)
			return self.send(show_in_interface_window=show_in_interface_window)

	def create_post_data(self, message_dict):
		self.post_data = str(json.dumps(message_dict)).encode('utf-8')

	def get_color_code(self, color_name):
		color_code = self.color_codes.get(color_name)
		return color_code if color_code else (255,0,0)

	def output_to_interface_window(self):
		self.display.fill(self.get_color_code(self.window_background_color))
		font = pg.font.Font(None, self.window_font_height)
		text = self.internal_message_dict["string"]
		if "main_color" in self.internal_message_dict:
			main_color = self.internal_message_dict["main_color"]
		else:
			main_color = None
		if not main_color:
			main_color = self.window_text_color
		output_text = font.render(text, True, self.get_color_code(main_color))
		self.display.blit(output_text, (10, 50))
		pg.display.update()

	def send(self, show_in_interface_window=True):
		if show_in_interface_window:
			self.output_to_interface_window()
		if not self.test_mode:
			req = self.get_POST_request()
			respond = self.make_request(req)
			if not respond:
				self.show_request_error_message()
			return respond
		else:
			return True
	
	def show_request_error_message(self):
		request_error_message = self.get_error_message(self.request_error_message_text)
		self.create_text_message_and_output_to_interface_window(request_error_message)

	def get_POST_request(self):
		return request.Request(self.full_led_server_address, data=self.post_data)

	def get_GET_request(self, pathname, external=False):
		if external:
			location = pathname
		else:
			location = '{}/{}'.format(self.full_led_server_address, pathname)
		return request.Request(location)

	def make_request(self, req):
		try:
			return request.urlopen(req)
		except Exception as request_error:
			print("Request error:", request_error)

	def download_json(self, pathname, external=False):
		req = self.get_GET_request(pathname, external)
		response = self.make_request(req)
		if isinstance(response, http.client.HTTPResponse) and response.status == 200:
			response_body = response.read().decode("utf-8")
			return json.loads(response_body)
		else:
			return False

	def set_level(self, level):
		self.level = level

	@classmethod
	def get_text_message(self, text=''):
		return {"string": text, "add_in_stack": False}

	@classmethod
	def get_colored_text_message(self, text, **kwargs):
		message = self.get_text_message(text)
		for color_target in ["main_color", "background_color", "letters_colors", "decorations"]:
			color = kwargs.get(color_target)
			if color:
				message[color_target] = color
		return message

	@classmethod
	def get_error_message(self, error_text):
		return self.get_colored_text_message(error_text, main_color='red')

	@classmethod
	def get_command_message(self, command):
		return {"command": command}

	def find_level(self, pathlist, level=False, level_number=0):
		if not level:
			level = self.zero_level
		level = level.get_item_by_classname(pathlist[level_number])
		if level_number < len(pathlist) - 1:
			return self.find_level(pathlist, level=level, level_number=level_number+1)
		else:
			return level

	def get_main_output_process_properties(self):
		self.main_output_process_properties = self.download_json("main_output_process_properties")
		return self.main_output_process_properties

	def merge_messages(self, main_message, additional_message, separator=" - "):

		def is_dict_with_proper_field(input_dict, field_name):
			if isinstance(input_dict, dict) and field_name in input_dict:
				return True
			else:
				return False

		def get_message_text(message):
			if is_dict_with_proper_field(message, text_field_name):
				return message[text_field_name]
			elif isinstance(message, str):
				return message
			else:
				return str(message)

		def get_additional_main_color(additional_message):
			if is_dict_with_proper_field(additional_message, main_color_field_name):
				return additional_message[main_color_field_name]
			else:
				return False

		def create_merged_message(main_message, merged_text):
			if not is_dict_with_proper_field(main_message, text_field_name):
				main_message = self.get_text_message(merged_text)
			else:
				main_message[text_field_name] = merged_text
			return main_message

		text_field_name = "string"
		main_color_field_name = "main_color"
		main_text = get_message_text(main_message)
		additional_text = get_message_text(additional_message)
		beginning_index = len(main_text) + len(separator)
		ending_index = beginning_index + len(additional_text) - 1
		
		merged_text = "{}{}{}".format(main_text, separator, additional_text)
		merged_message = create_merged_message(main_message, merged_text)
		
		additional_main_color = get_additional_main_color(additional_message)
		if additional_main_color:
			merged_message["letters_colors"] = {main_color_field_name: {additional_main_color: ["{}-{}".format(beginning_index, ending_index)]}}
		return merged_message

	def refresh_text(self, pronounce=True):
		self.send_text_message(self.last_text_message, self.last_letter_case_method, pronounce)

	def pronounce(self, text, lang=False):
		if self.pronunciation_manager:
			if not text:
				text = self.last_text_message["string"]
			self.pronunciation_manager.pronounce(text, lang)

	def pronunciation_pause(self):
		if self.pronunciation_manager:
			self.pronunciation_manager.pronunciation_pause()

	def listen_to_keys(self):
		while True:
			for i in pg.event.get():
				if i.type == pg.KEYUP:
					if self.start_available:
						if i.key == self.get_key("main_menu"):
							# immediately open main menu
							self.zero_level.open()
						elif i.key == self.get_key("up"):
							self.level.up()
						elif i.key == self.get_key("down"):
							self.level.down()
						elif i.key == self.get_key("left"):
							self.level.left()
						elif i.key == self.get_key("right"):
							self.level.right()
						elif i.key == self.get_key("activate"):
							self.level.activate()
						elif i.key == self.get_key("back"):
							self.level.back()
						elif i.key == self.get_key("refrest_text"):
							self.refresh_text()
						elif i.key == self.get_key("pronounce"):
							self.level.pronounce()
						elif i.key == self.get_key("pronunciation_pause"):
							self.pronunciation_pause()
					if i.key == self.get_key("close"):
						# close interface application level
						pg.quit()
						sys.exit()

User_Interface()