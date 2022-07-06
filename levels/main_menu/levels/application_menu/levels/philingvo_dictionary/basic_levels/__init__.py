#coding: utf-8

import functools
from levels.basic_levels import Level
from levels.basic_levels import Level_with_Downloading
from levels.basic_levels import Application_Level_With_User_Settings


class Basic_Philingvo_Level_With_Downloading(Level_with_Downloading, Application_Level_With_User_Settings):

	address = "127.0.0.1:8050"
	address = None
	location = None
	next_level_class = None
	main_container_field = None
	param_name = None
	path = None
	query_string_path = None
	query_string_value = True
	response_format = list
	fields = []
	language_code_path = None
	field_position = 0
	application_name = "philingvo_dictionary"
	user_settings = ["address"]
	location_template = "http://{}/api/{}/"

	format_error_text = "Wrong response format"
	field_error_text = "Fields haven't been assigned"
	no_address_error_text = "No address to connect to a server"
	no_path_error_text = "Path hasn't been assigned"
	empty_field_text_template = "{} is empty"
	loading_text_template = "Loading {}"
	no_fields_text_text = "No {} fields in item"

	def __init__(self, previous_level):
		super().__init__(previous_level)
		self.assign_user_settings()

	def open(self, **kwargs):
		if self.query_string_value:
			self.query_string_value = kwargs['item_id']
		self.copy_input_params(kwargs)
		self.send_loading_text()
		self.create_path()
		super().open()

	def copy_input_params(self, kwargs):
		self.params = kwargs

	def send_loading_text(self, target=False):
		if not target:
			target = self.name
		self.send_text_message(self.loading_text_template.format(target), pronounce=False)

	def create_path(self):

		if self.address:
			if self.path:
				self.location = self.location_template.format(self.address, self.path)
				if self.query_string_path:
					self.location = "{}?{}={}".format(self.location, self.query_string_path, self.query_string_value)
			else:
				self.send_error_message(self.no_path_error_text)
		else:
			self.send_error_message(self.no_address_error_text)

	def download_json(self):
		if self.location:
			self.response = self.interface.download_json(self.location, True)
		if len(self.response) == 0:
			self.send_error_message("No {} hasn't been created yet".format(self.param_name))

	def check_response(handle_method):

		@functools.wraps(handle_method)
		def wrapper(self):
			if self.response_format and isinstance(self.response, self.response_format):
				self.items = handle_method(self)
			else:
				message_dict = self.interface.get_error_message(self.format_error_text)
				self.send_text_message(message_dict)

		return wrapper

	def get_item(self):
		return self.items[self.item_position]

	def get_field_text(self, input_field_name=False, assign_pronunciation_lang=False):
		item = self.get_item()
		if len(self.fields) == 0:
			field_name = "name"
		elif input_field_name:
			field_name = input_field_name
		else:
			field_name = self.fields[self.field_position]

		if assign_pronunciation_lang:
			self.assign_item_language_for_pronunciation()

		if field_name:
			if isinstance(field_name, str):
				field_text = self.extract_field(item, field_name)
			elif isinstance(field_name, list):
				internal_field_names = self.check_field_name(field_name)

				if len(internal_field_names) < 2:
					field_name_index = 1
				else:
					field_name_index = -1

				field_name = field_name[field_name_index]

				if field_name_index < 0:
					start_field_name = internal_field_names[field_name_index - 1]
					field_name = "{} {}".format(start_field_name, field_name)
				for internal_field_name in internal_field_names:
					item = self.extract_field(item, internal_field_name)
					if isinstance(item, str) or item is None:
						field_text = item
					else:
						field_text = str(item)
			else:
				field_text = False
		else:
			field_text = False
		
		if input_field_name:
			if field_text:
				return field_text
			else:
				return None
		else:
			field_name = field_name.replace("_", " ")
			if field_text:
				return "{} - {}".format(field_text, field_name)
			elif field_text == "":
				return self.empty_field_text_template.format(field_name)
			else:
				return self.field_error_text

	def check_field_name(self, field_name):
		if self.main_container_field:
			if isinstance(field_name, str):
				field_name = [field_name]
			if field_name[0] != self.main_container_field:
				field_name.insert(0, self.main_container_field)
		return field_name

	def extract_field(self, item, field_name):
		if field_name in item:
			return item[field_name]
		else:
			return self.no_fields_text_text.format(field_name)

	def get_item_id(self):
		field_name = self.check_field_name('id')
		return self.get_field_text(field_name)

	def get_item_color(self):
		field_name = self.check_field_name('color')
		return self.get_field_text(field_name)

	def get_item_title(self):
		text = self.get_field_text(assign_pronunciation_lang=True)
		message_dict = self.interface.get_text_message(text)
		color = self.get_item_color()
		if color:
			message_dict["main_color"] = color
		return message_dict

	def right(self):
		if len(self.fields) > 0:
			self.field_position += 1
			if self.field_position >= len(self.fields):
				self.field_position = 0
			self.show_item_title()

	def left(self):
		if len(self.fields) > 0:
			self.field_position -= 1
			if self.field_position < 0:
				self.field_position = len(self.fields) - 1
			self.show_item_title()

	@check_response
	def handle_response(self):
		return self.response

	def activate(self):
		if len(self.items) > 0 and self.next_level_class:
			self.open_next_level()

	def prepare_output_params(self):
		self.params["item_id"] = self.get_item_id()
		if self.param_name:
			self.params[self.param_name] = {"id": self.params["item_id"],
											"title": self.get_field_text(),
											"language": self.get_language_code()
											}

	def open_next_level(self):
		self.prepare_output_params()
		next_level = self.next_level_class(self)
		next_level.open(**self.params)

	def get_language_code(self):
		if "language" in self.fields:
			return self.get_field_text("language")
		elif self.language_code_path:
			return self.get_field_text(self.language_code_path)
		else:
			return None

	def assign_item_language_for_pronunciation(self):
		lang_code = self.get_language_code()
		self.assign_language_for_pronunciation(lang_code)

class Choosing_Level(Level):

	param_name = None
	next_level_class = None

	no_next_level_class_error_text = "Can't open next level. Next level class hasn't been assigned"

	def open(self, **kwargs):
		self.copy_input_params(kwargs)
		super().open()

	def comeback(self):
		self.set_level()
		self.show_level_name()

	def copy_input_params(self, kwargs):
		self.params = kwargs

	def show_first_item(self):
		self.item_position = 0
		self.item_class = self.get_item_class()
		self.show_level_name()

	def show_level_name(self):
		item_title_message = self.get_class_title(self.item_class)
		level_name_message = self.get_class_title(self.__class__)
		message = self.merge_messages(item_title_message, level_name_message, ": ")
		self.send_text_message(message)

	def left(self):
		self.show_level_name()

	def right(self):
		self.show_level_name()

	def activate(self):
		if len(self.items) > 0 and self.next_level_class:
			self.open_next_level()
		else:
			self.send_error_message(self.no_next_level_class_error_text)

	def open_next_level(self):
		next_level = self.next_level_class(self)
		self.open_level(next_level)

	def open_level(self, level):
		if self.param_name:
			self.params[self.param_name] = self.get_item_name_text(self.item_class)
		level.open(**self.params)

class Intermediary_Choosing_Level(Choosing_Level):

	def show_first_item(self):
		pass

	def open(self, **kwargs):
		super().open(**kwargs)
		self.open_next_level()

	def comeback(self):
		self.previous_level.comeback()