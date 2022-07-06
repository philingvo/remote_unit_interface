#coding: utf-8

import math
import json
import random
import functools
from levels.basic_levels import Level
from ...basic_levels import Basic_Philingvo_Level_With_Downloading
from ...basic_levels import Choosing_Level
from .info_fields import Part_Info_Menu_Level
from .info_fields import Activity_Menu
from .info_fields import Part_Info_Menu
from .info_fields import Set_Info_Menu
from .info_fields import Slice_Info_Menu


class Basic_Activity(Basic_Philingvo_Level_With_Downloading, Choosing_Level):
	name = "activity mode"
	path = "set_with_elements"
	activity_name = None
	downloading_target = "set"
	query_string_path = "set_id"
	response_format = dict
	
	element = None
	part = None
	element_position = 0
	part_position = 0
	attempt = 0
	attempts = 1

	general_params_name = ["set_id",
							"max_slice_length",
							"slice_position",
							"slice_length",
							"slice_title",
							"elements_order",
							"parts_order",
							"mode_name",
							"using_part_decorations"]

	set_params_names = ["items",
						"set_length",
						"element_length",
						"set_properties",
						"parts_types"]

	info_position = 0
	current_info_field = None

	no_part_info_field_template = "No part {} yet"
	no_elements_in_set_error_text = "No elements in set"
	mode_is_finished_text = "Mode is finished"
	mode_is_begun_text = "Mode's beginning"
	no_information_error_text = "This information field can't be shown nor opened"
	no_info_text = "No text"
	no_abstract_text = "No abstract yet"

	def __init__(self, previous_level):
		super().__init__(previous_level)
		self.info_fields = ["item_title",
							"comment",
							Activity_Menu,
							Part_Info_Menu,
							Set_Info_Menu,
							Slice_Info_Menu]
	
	def open(self, **kwargs):
		self.copy_input_params(kwargs)
		self.assign_param()
		self.set_level()
		if "items" in self.params:
			self.copy_set_params_to_activity()
			self.show_first_item()
		else:
			self.send_loading_text()
			self.set_start_positions()
			self.create_path()
			self.create_items()

	def reopen(self, command=False):
		self.set_level()
		if command:
			method = self.run_show_method(command, True)
		else:
			self.info_position = 0
			self.show_part_text()

	def reopen_and_show_info_field_item(self):
		self.set_level()
		self.show_info_field()

	def reopen_last_step(self):
		self.set_level()
		self.info_position = 0
		if self.part_position < self.current_element_length:
			self.show_part_text()
		else:
			self.left()

	def set_start_positions(self):
		self.attempt = 0
		self.part_position = 0
		self.element_position = 0

	def assign_param(self):
	
		self.copy_general_params_to_activity()
		self.query_string_value = self.set_id
		self.additional_params = self.params.get("additional_params")

	def copy_params_to_activity(self, params_name):
		for param_name in params_name:
			self.__setattr__(param_name, self.params[param_name])

	def copy_set_params_to_activity(self):
		self.copy_params_to_activity(self.set_params_names)

	def copy_general_params_to_activity(self):
		self.copy_params_to_activity(self.general_params_name)

	def copy_set_params_from_activity(self):
		for set_param_name in self.set_params_names:
			self.params[set_param_name] = self.__getattribute__(set_param_name)

	def sort_elements(self):
		elements_order = self.get_current_activity_param_value("elements_order")
		if elements_order == "direct":
			sorting_function = lambda element: element["position"]
		elif elements_order == "reverse":
			sorting_function = lambda element: -1 * element["position"]
		elif elements_order == "shuffle":
			sorting_function = lambda element: random.random()
		self.items = sorted(self.items, key=sorting_function)

	def create_path(self):
		super().create_path()
		if self.slice_position != 'all':
			self.location = '{}&slice_position={}&slice_length={}'.format(self.location,
																		self.slice_position,
																		self.max_slice_length)

	def get_current_activity_param_value(self, param_name):
		if self.additional_params and param_name in self.additional_params:
			return self.additional_params[param_name]
		else:
			return self.__getattribute__(param_name)

	@Basic_Philingvo_Level_With_Downloading.check_response
	def handle_response(self):
		if "elements" in self.response and "set" in self.response:
			elements = self.response["elements"]
			self.set_length = len(elements)
			self.element_length = len(self.response["set"]["parts_types"])
			self.set_properties = self.response['set']['set_properties']
			self.parts_types = self.response["set"]["parts_types"]
			return self.response["elements"]

	def show_first_item(self):
		self.sort_elements()
		self.show_part_text()

	def show_part_text(self):
		self.set_part()
		self.show_item_title()

	def show_item_title(self):
		self.assign_language_for_pronunciation(self.part_language["code"])
		super().show_item_title()

	def get_part_prop(self, prop_name):
		content = self.part[prop_name]
		if not content:
			content = self.no_part_info_field_template.format(prop_name)
		return content

	def get_part_content(self):
		return self.get_part_prop("content")

	def get_part_comment(self):
		return self.get_part_prop("comment")

	def get_part_styles(self):
		# only for text parts is this part style is "text"
		# if there's no styles for this part try to find styles for the first part
		# if there's no styles even for the first part try to find styles for set part number() ["set"]["part_types"][this_part_number]["type"]["main_color"] // ["background_color"]
		# use code from output_process
		styles = self.part.get("style")
		return json.loads(styles) if styles else dict()

	def get_item_title_message(self):
		if self.set_length > 0:
			part_content = self.get_part_content()
			self.styles = self.get_part_styles()

			if self.using_part_decorations.lower() == "no" and "decorations" in self.styles:
				del self.styles["decorations"]

			return self.interface.get_colored_text_message(part_content, **self.styles)
		else:
			return self.interface.get_error_message(self.no_elements_in_set_error_text.format(self.set_title))

	def show_comment(self):
		comment = self.get_part_comment()
		message = self.interface.get_colored_text_message(comment, **self.styles)
		self.assign_language_for_pronunciation(self.part_language["code"])
		self.send_text_message(message)

	def set_element(self):
		self.element = self.items[self.element_position]
		self.current_element_length = len(self.element["parts"])

	def set_part(self):
		self.set_element()
		parts_order = self.get_current_activity_param_value("parts_order")
		if parts_order == "direct":
			part_position = self.part_position
		elif parts_order == "reverse":
			part_position = self.element_length - self.part_position - 1
		self.part = self.element["parts"][part_position]["part"]
		self.part_language = self.parts_types[part_position]["type"]["language"]

	def next_part(self):
		self.part_position += 1
		if self.part_position >= self.current_element_length:
			self.part_position = 0
			self.next_mode_action()
		else:
			self.send_part()

	def next_mode_action(self):
		pass

	def next_element(self):
		self.element_position += 1
		if self.element_position >= self.slice_length:
			self.element_position -= 1
			self.next_attempt()
		else:
			self.send_part()

	def next_attempt(self):
		self.attempt += 1
		if self.attempt >= self.attempts:
			self.attempt = self.attempts - 1
			self.next_activity()
		else:
			self.element_position = 0
			self.send_part()

	def next_activity(self):
		self.attempt = self.attempts - 1

		if self.previous_level.is_last_activity_position:
			self.part_position = self.current_element_length # if this activity part is the last
			message = self.interface.get_colored_text_message(self.mode_is_finished_text, main_color="green")
			self.send_text_message(message)
			self.previous_level.open_final_activity_menu()
		else:
			self.part_position = self.current_element_length - 1
			self.copy_set_params_from_activity()
			self.previous_level.next_activity(**self.params)

	def send_part(self):
		self.set_part()
		self.show_item_title()

	def right(self):
		self.next_part()

	def previous_part(self):
		self.part_position -= 1
		if self.part_position < 0:
			self.part_position = self.current_element_length - 1
			self.previous_mode_action()
		else:
			self.send_part()

	def previous_mode_action(self):
		pass

	def previous_element(self):
		self.element_position -= 1
		if self.element_position < 0:
			self.previous_attempt()
		else:
			self.send_part()

	def previous_attempt(self):
		self.attempt -= 1
		if self.attempt < 0:
			self.previous_activity()
		else:
			self.element_position = self.slice_length - 1
			self.send_part()

	def previous_activity(self):
		self.set_start_positions()

		if self.previous_level.is_first_activity_position:
			message = self.interface.get_colored_text_message(self.mode_is_begun_text, main_color="green")
			self.send_text_message(message)
			self.previous_level.open_final_activity_menu()
		else:
			self.copy_set_params_from_activity()
			self.previous_level.previous_activity(**self.params)

	def left(self):
		self.previous_part()

	def up(self):
		self.info_position -= 1
		if self.info_position < 0:
			self.info_position = len(self.info_fields) - 1
		self.show_info_field()
	
	def down(self):
		self.info_position += 1
		if self.info_position >= len(self.info_fields):
			self.info_position = 0
		self.show_info_field()

	def activate(self):
		if self.current_info_field:
			self.current_info_field.open()
		else:
			self.right()

	def run_show_method(self, command, show_info_name=False):
		show_method_name = "show_{}".format(command.lower().replace(" ", "_"))
		show_method = self.__getattribute__(show_method_name)
		show_method(command) if show_info_name else show_method()

	def get_info_field_message(self):
		return False

	def show_info_field(self):
		
		self.assign_level_language_for_pronunciation()
		info_item = self.info_fields[self.info_position]
		if isinstance(info_item, str):
			self.current_info_field = False
			method = self.run_show_method(info_item)
		elif issubclass(info_item, Part_Info_Menu_Level):
			self.current_info_field = info_item(self)
			self.current_info_field.show_menu_title()
		else:
			self.send_error_message(self.mode_is_finished_text)

	def send_info_field_decorator(show_method):

		@functools.wraps(show_method)
		def wrapper(self, info_name):
			info_text = show_method(self, info_name)
			if not info_text:
				info_text = self.no_info_text
			self.send_text_message("{} - {}".format(info_text, info_name.capitalize()))

		return wrapper

	def assign_set_language_for_pronunciation_decorator(show_method):

		functools.wraps(show_method)
		def wrapper(self, *args):
			self.assign_language_for_pronunciation(self.set_properties["type"]["language"]["code"])
			show_method(self, *args)

		return wrapper

	@send_info_field_decorator
	def show_part_position(self, info_name):
		return self.part_position + 1

	@send_info_field_decorator
	def show_part_name(self, info_name):
		return self.parts_types[self.part_position]["type"]["name"]

	@send_info_field_decorator
	def show_part_format(self, info_name):
		return self.parts_types[self.part_position]["type"]["format"]["name"]

	@send_info_field_decorator
	def show_part_language(self, info_name):
		self.assign_language_for_pronunciation(self.part_language["code"])
		return self.part_language["original_name"]

	@assign_set_language_for_pronunciation_decorator
	@send_info_field_decorator
	def show_set_title(self, info_name):
		return self.set_properties["title"]

	@assign_set_language_for_pronunciation_decorator
	@send_info_field_decorator
	def show_set_type(self, info_name):
		return self.set_properties["type"]["name"]

	@assign_set_language_for_pronunciation_decorator
	@send_info_field_decorator
	def show_set_abstract(self, info_name):
		abstract = self.set_properties["abstract"]
		if not abstract:
			abstract = self.no_abstract_text
		return abstract

	@assign_set_language_for_pronunciation_decorator
	@send_info_field_decorator
	def show_set_language(self, info_name):
		return self.set_properties["type"]["language"]["original_name"]

	@assign_set_language_for_pronunciation_decorator
	@send_info_field_decorator
	def show_set_abstract(self, info_name):
		abstract = self.set_properties["type"]["abstract"]
		if not abstract:
			abstract = self.no_abstract_text
		return abstract

	@send_info_field_decorator
	def show_set_id(self, info_name):
		return self.set_properties["id"]

	def show_container_title(self, container_name):
		if container_name in self.params:
			container = self.params[container_name]
			self.assign_language_for_pronunciation(container["language"])
			return "{}: {} ({})(ID:{})".format(container_name,
												container["title"],
												container["language"],
												container["id"])
		else:
			return False

	@send_info_field_decorator
	def show_topic_title(self, info_name):
		return self.show_container_title("topic")

	@send_info_field_decorator
	def show_subject_title(self, info_name):
		return self.show_container_title("subject")

	@send_info_field_decorator
	def show_playlist_title(self, info_name):
		return self.show_container_title("playlist")

	@send_info_field_decorator
	def show_element_position(self, info_name):
		return self.element_position + 1

	@send_info_field_decorator
	def show_slice_position(self, info_name):
		return self.slice_position

	@send_info_field_decorator
	def show_slice_length(self, info_name):
		return self.slice_length

	@send_info_field_decorator
	def show_slice_title(self, info_name):
		return self.slice_title

	@send_info_field_decorator
	def show_mode_name(self, info_name):
		return self.mode_name

	@send_info_field_decorator
	def show_activity_name(self, info_name):
		return self.activity_name

	@send_info_field_decorator
	def show_elements_order(self, info_name):
		return self.elements_order

	@send_info_field_decorator
	def show_parts_order(self, info_name):
		return self.parts_order
	
	def show_final_activity_menu(self, info_name=None):
		self.previous_level.open_final_activity_menu()

class Revision_Activity(Basic_Activity):

	activity_name = "Revision"

	def next_mode_action(self):
		self.next_element()

	def previous_mode_action(self):
		self.previous_element()

	def next_activity(self):
		self.element_position = self.slice_length - 1
		super().next_activity()

class Memorizing_Activity(Basic_Activity):

	activity_name = "Memorizing"

	chunks = None
	chunk_position = 0

	chunk_length = None
	max_chunk_length = None
	chunk_element_position = 0

	chunk_attempts = 2
	chunk_attempt = 0

	def assign_param(self):
		super().assign_param()
		self.max_chunk_length = 5

		self.full_chunks = self.slice_length // self.max_chunk_length
		self.chunks = math.ceil(self.slice_length / self.max_chunk_length)

	def next_mode_action(self):
		self.next_chunk_element()

	def previous_mode_action(self):
		self.previous_chunk_element()

	def show_part_text(self):
		self.define_chunk_length()
		super().show_part_text()

	def define_chunk_length(self):
		if self.chunk_position >= self.full_chunks and self.full_chunks < self.chunks: # the last chunk
			self.chunk_length = self.slice_length % self.max_chunk_length
		else:
			self.chunk_length = self.max_chunk_length

	def next_chunk_element(self):
		self.chunk_element_position += 1
		if self.chunk_element_position >= self.chunk_length:
			self.chunk_element_position = 0
			self.next_chunk_attempt()
		else:
			self.next_element()

	def next_chunk_attempt(self):
		self.chunk_attempt += 1
		if self.chunk_attempt >= self.chunk_attempts:
			self.next_chunk()
		else:
			self.element_position -= self.chunk_length
			self.next_element()

	def next_chunk(self):
		self.chunk_position += 1
		if self.chunk_position >= self.chunks:
			self.next_activity()
		else:
			self.chunk_attempt = 0
			self.define_chunk_length()
			self.next_element()

	def next_activity(self):
		super().next_activity()
		self.chunk_element_position = self.chunk_length - 1
		self.chunk_attempt = self.chunk_attempts - 1
		self.chunk_position = self.chunks - 1

	def previous_chunk_element(self):
		self.chunk_element_position -= 1
		if self.chunk_element_position < 0:
			self.previous_chunk_attempt()
		else:
			self.previous_element()

	def previous_chunk_attempt(self):
		self.chunk_attempt -= 1
		if self.chunk_attempt < 0:
			self.previous_chunk()
		else:
			self.chunk_element_position = self.chunk_length - 1
			self.element_position += self.chunk_length
			self.previous_element()

	def previous_chunk(self):
		self.chunk_position -= 1
		if self.chunk_position < 0:
			self.chunk_element_position = 0
			self.part_position = 0
			self.previous_activity()
		else:
			self.chunk_attempt = self.chunk_attempts - 1
			self.define_chunk_length()
			self.chunk_element_position = self.chunk_length - 1
			self.previous_element()

	def set_start_positions(self):
		super().set_start_positions()
		self.chunk_element_position = 0
		self.chunk_attempt = 0
		self.chunk_position = 0