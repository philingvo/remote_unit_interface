#coding: utf-8

class Level():

	name = ""
	items = []
	main_color = None
	background_color = None
	letters_colors = None
	item_position = 0
	changeable_items = []
	item_class = None
	language = None
	language_for_pronunciaition = None

	item_type_names = "items"

	def __init__(self, previous_level):
		self.previous_level = previous_level
		self.find_interface()
		self.change_items_names()

	def find_interface(self):
		if isinstance(self.previous_level, Level):
			self.interface = self.previous_level.interface
		else:
			self.interface = self.previous_level
			self.previous_level = False

	def set_level(self):
		self.interface.set_level(self)

	def open(self):
		self.set_level()
		self.show_first_item()

	def comeback(self):
		self.set_level()
		self.show_item_title()
	
	def show_first_item(self):
		self.item_position = 0
		self.show_item_title()

	@classmethod
	def get_colored_title(self, interface, title=False):
		if not title:
			title = self.name
		message_dict = interface.get_text_message(title)
		for color_target in ["main_color", "background_color", "letters_colors"]:
			color = getattr(self, color_target)
			if color:
				message_dict[color_target] = color
		return message_dict

	def get_item_class(self):
		return self.items[self.item_position]

	def show_item_title(self):
		message = self.get_item_title_message()
		self.send_text_message(message)

	def get_item_title(self):
		self.item_class = self.get_item_class()
		self.assign_item_language_for_pronunciation(self.item_class)
		return self.get_class_title(self.item_class)

	def assign_item_language_for_pronunciation(self, item_class):
		if isinstance(item_class, type) and issubclass(item_class, Level):
			self.assign_language_for_pronunciation(item_class.language)

	def get_class_title(self, item_class, title_field_name=None):
		if isinstance(item_class, type) and issubclass(item_class, Level):
			if item_class.main_color or item_class.background_color:
				return item_class.get_colored_title(self.interface)
			else:
				return item_class.name
		elif isinstance(item_class, str):
			return item_class
		elif isinstance(item_class, dict) and title_field_name:
			return item_class[title_field_name]
		else:
			return str(item_class)

	def get_item_name_text(self, item_class):
		if isinstance(item_class, type) and issubclass(item_class, Level):
			return item_class.name
		elif isinstance(item_class, str):
			return item_class
		else:
			return str(item_class)

	@classmethod
	def get_item_by_classname(self, classname):
		for item in self.items:
			if issubclass(item, Level):
				item_id = item.__name__
			elif isinstance(item, str):
				item_id = item
			if item_id == classname:
				return item
		return None

	def get_item_title_message(self):
		if len(self.items) > 0:
			return self.get_item_title()
		else:
			return self.get_no_items_error_message()

	def get_no_items_error_message(self):
		no_items_text = "No {} in {}".format(self.item_type_names, self.name)
		return self.interface.get_error_message(no_items_text)

	def send_text_message(self, message, letter_case_method=True, pronounce=True):
		self.interface.send_text_message(message, letter_case_method, pronounce)

	def send_error_message(self, error_text):
		self.interface.send_error_message(error_text)

	def change_items_names(self):
		if len(self.changeable_items) > 0:
			main_output_process_properties = self.interface.get_main_output_process_properties()
			if main_output_process_properties:
				for changeable_item in self.changeable_items:
					property_name = self.interface.changeable_items_names.get(changeable_item.__name__)
					if property_name:
						changeable_item.change_name(main_output_process_properties[property_name])

	def change_name(self, property_value):
		pass

	def down(self):
		self.item_position += 1
		if self.item_position >= len(self.items):
			self.item_position = 0
		self.show_item_title()

	def up(self):
		self.item_position -= 1
		if self.item_position < 0:
			self.item_position = len(self.items) - 1
		self.show_item_title()

	def left(self):
		pass

	def right(self):
		pass

	def activate(self):
		if len(self.items) > 0:
			item = self.item_class(self)
			item.open()

	def back(self):
		if self.previous_level:
			self.previous_level.comeback()

	def merge_messages(self, *args):
		return self.interface.merge_messages(*args)

	def get_colored_text_message(self, text, **kwargs):
		return self.interface.get_colored_text_message(text, **kwargs)

	def assign_language_for_pronunciation(self, language_code=None):
		self.language_for_pronunciaition = language_code

	def assign_level_language_for_pronunciation(self):
		self.assign_language_for_pronunciation(self.language)

	def pronounce(self, text=False, lang=False):
		if not lang:
			lang = self.language_for_pronunciaition
		if not lang:
			lang = self.language
		self.interface.pronounce(text, lang)

class Command(Level):

	command = None
	open_background_color = "green"
	use_open_background_color = False

	no_command_error_text = "Сommand hasn't been assign to send"

	def open(self):
		if self.command:
			if self.use_open_background_color and self.open_background_color:
				message = self.get_colored_title()
				message["background_color"] = self.open_background_color
				self.send_text_message(message)
			self.interface.send_command(self.command)
		else:
			self.send_error_message(self.no_command_error_text)

class Basic_Change_Status_Command(Command):

	status = False
	letters_colors = {"main_color":{}}
	name_template = "{}"

	on_text = "ON"
	off_text = "OFF"

	@classmethod
	def get_command_text(self):
		return self.off_text if self.status else self.on_text

	@classmethod
	def fill_letters_colors(self):
		color_range = {"red": ["5-7"]} if self.status else {"green": ["5-6"]}
		self.letters_colors["main_color"] = color_range

	@classmethod
	def change_name(self, status):
		self.status = status
		self.name = self.name_template.format(self.get_command_text())
		self.fill_letters_colors()

	def open(self):
		super().open()
		status = not self.status
		self.__class__.change_name(status)
		self.send_text_message(self.previous_level.get_item_title())

class Level_with_Downloading(Level):

	pathname = None
	response = None
	item_key = None
	downloading_target = None
	
	downloading_error_text_template = "{} can't be downloaded"
	no_downloading_target_error_text = "Downloading can't be implemented"
	no_pathname_error_text = "Pathname hasn't been assign"

	def open(self):
		self.set_level()
		self.create_items()

	def create_items(self):
		self.download_json()
		if self.response or isinstance(self.response, (list, dict)):
			self.handle_response()
			if len(self.items):
				self.show_first_item()
		else:
			if self.downloading_target:
				error_text = self.downloading_error_text_template.format(self.downloading_target)
			else:
				error_text = self.no_downloading_target_error_text
			message_dict = self.interface.get_error_message(error_text)
			self.send_text_message(message_dict)

	def handle_response(self):
		if isinstance(self.response, list):
			self.items = []
			for item in self.response:
				item_title = item[self.item_key].replace("_", " ") if self.item_key else str(item)
				self.items.append(item_title)
		elif isinstance(self.response, dict):
			self.items = self.response.keys()

	def download_json(self):
		if self.pathname:
			self.response = self.interface.download_json(self.pathname)
		else:
			self.send_error_message(self.no_pathname_error_text)

	def activate(self):
		if len(self.items) > 0:
			command_dict = self.get_command_dict()
			if command_dict:
				self.interface.send_command(command_dict)

	def get_command_dict(self):
		return False

	def get_item_title(self):
		self.item_class = self.get_item_class()
		message_dict = self.interface.get_text_message(self.item_class)
		colors = sorted(list(self.interface.color_codes.keys()))
		default_background_color = self.interface.window_settings["background_color"]
		if default_background_color in colors:
			index = colors.index(default_background_color)
			colors = colors[:index] + colors[index + 1:]
		message_dict["main_color"] = colors[self.item_position % len(self.interface.color_codes)]
		return message_dict

class Yes(Level):
	name = "yes"
	main_color = "red"

class No(Level):
	name = "no"
	main_color = "green"

class Quit_Choice_Basic(Level):

	def open(self):
		self.previous_level.comeback(self.command)

class No_Quit_Choice(No, Quit_Choice_Basic):
	command = False

class Yes_Quit_Choice(Yes, Quit_Choice_Basic):
	command = True

class Quit_Menu(Level):
	items = [No_Quit_Choice, Yes_Quit_Choice]
	default_item_position = 0
	name = "quit"
	question_text_template = "Stop {}?"
	main_color = "purple"
	now_question = False

	def open(self):
		self.set_level()
		self.default_item_class = self.items[self.default_item_position]
		self.create_question_text()
		self.set_question()

	def create_question_text(self):
		question_message = self.get_colored_title(self.interface, self.question_text)
		choice_message = self.default_item_class.get_colored_title(self.interface)
		self.question_text_message = self.merge_messages(question_message, choice_message)

	def set_question(self):
		self.now_question = True
		self.item_class = self.default_item_class
		self.send_text_message(self.question_text_message)

	@property
	def question_text(self):
		return self.question_text_template.format("")

	def comeback(self, command=False):
		if command:
			self.escape()
		else:
			self.resume()

	def escape(self):
		self.previous_level.escape()

	def resume(self):
		self.previous_level.resume()

	def switch_question(self):
		if self.now_question:
			self.show_item_title()
		else:
			self.set_question()

	def show_item_title(self):
		self.now_question = False
		super().show_item_title()

	def left(self):
		self.switch_question()

	def right(self):
		self.switch_question()

	def back(self):
		self.go_to_activity_level()

class Application_Level_With_User_Settings(Level):

	application_name = None
	user_settings = None

	def assign_user_settings(self):
		if isinstance(self.interface.application_settings, dict) and self.application_name in self.interface.application_settings:
			application_settings = self.interface.application_settings[self.application_name]
			if isinstance(application_settings, dict):
				for user_setting in self.user_settings:
					if user_setting in application_settings:
						self.address = application_settings[user_setting]

class Interface_Setting_Choosing_Level(Level):
	
	setting_name = None
	check_value = None

	def change_setting_value(self, new_value):
		self.interface.__setattr__(self.setting_name, new_value)

	def activate(self):
		if len(self.items) > 0 and self.setting_name and "value" in self.item_class.__dict__:
			value = self.item_class.value
			if self.is_interface_setting_name() and self.is_value_possible(value):
				self.change_setting_value(value)
				self.back()

	def is_interface_attribute(self, attribure_name):
		return attribure_name in self.interface.__class__.__dict__

	def is_interface_setting_name(self):
		return self.is_interface_attribute(self.setting_name)

	def is_value_possible(self, value):
		if self.check_value:
			possible_values_attribute_name = "possible_{}".format(self.setting_name)
			if self.is_interface_attribute(possible_values_attribute_name):
				possible_values = getattr(self.interface, possible_values_attribute_name)
				if isinstance(possible_values, (list, tuple)) and value in possible_values:
					return True
				else:
					return False
			else:
				return False
		else:
			return True