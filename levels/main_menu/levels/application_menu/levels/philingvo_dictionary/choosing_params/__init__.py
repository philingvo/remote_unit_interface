#coding: utf-8

from levels.basic_levels import Level
from levels.basic_levels import Yes
from levels.basic_levels import No
from ..basic_levels import Basic_Philingvo_Level_With_Downloading
from ..basic_levels import Choosing_Level
from ..basic_levels import Intermediary_Choosing_Level
from ..process import Process
import time


class Choosing_Part_Decorations(Choosing_Level):
	name = "use part decorations"
	main_color = "yellow"
	param_name = "using_part_decorations"
	items = [
			No,
			Yes
			]
	next_level_class = Process

class Choosing_Slice_Number(Choosing_Level, Basic_Philingvo_Level_With_Downloading):
	name = "slice position"
	main_color = "pink"
	param_name = "slice_title"
	query_string_path = "set_id"
	path = downloading_target = "set_length"
	next_level_class = Choosing_Part_Decorations
	items = []

	set_length = None
	slice_length = None
	slice_text = None

	all_text = "All elements"
	no_set_length_text = "Can't find set length"

	def open(self, **kwargs):
		self.copy_input_params(kwargs)
		self.query_string_value = self.params["set_id"]
		if "slice_length" in self.params and self.params["slice_length"] != "all":
			slice_length = int(self.params["slice_length"])
		else:
			slice_length = "all"
		self.slice_length = self.params["max_slice_length"] = slice_length

		if slice_length == "all":
			self.slice_text = self.all_text

		self.send_loading_text(self.downloading_target.replace("_", " "))
		self.create_path()
		super(Basic_Philingvo_Level_With_Downloading, self).open()

	def handle_response(self):
		if isinstance(self.response, dict) and self.downloading_target in self.response:
			self.set_length = int(self.response[self.downloading_target])
			if self.set_length == 0:
				self.send_error_message("This set has no elements")
				time.sleep(2)
				self.previous_level.previous_level.previous_level.previous_level.comeback()
			else:
				self.create_slice_parts_as_items()
		else:
			error_text = self.no_set_length_text
			message_dict = self.interface.get_error_message(error_text)
			self.send_text_message(message_dict)
			# back to previous level

	def get_slice_title(self, slice_position_text, slice_position, slice_length):
		return {self.param_name: "{}({})".format(slice_position_text, slice_length),
				"slice_position": slice_position,
				"slice_length": slice_length}

	def add_item(self, slice_number_text, slice_number, slice_length):
		self.items.append(self.get_slice_title(slice_number_text, slice_number, slice_length))

	def add_all_elements_item(self):
		self.add_item(self.all_text.capitalize(), 'all' , self.set_length)

	def clean_items(self):
		if len(self.items) > 0:
			self.items = []

	def create_slice_parts_as_items(self):

		self.clean_items()

		if self.slice_length != "all":
			full_slices = self.set_length // self.slice_length
			if full_slices > 0:
				for slice_number in range(1, full_slices + 1):
					self.add_item(slice_number, slice_number, self.slice_length)

			rest_elements = self.set_length % self.slice_length
			if rest_elements > 0:
				self.add_item(full_slices + 1, full_slices + 1, rest_elements)
		
		self.add_all_elements_item()

	def get_item_title(self):
		return Level.get_item_title(self)

	def get_class_title(self, item):
		return Level.get_class_title(self, item, self.param_name)

	def activate(self):
		Basic_Philingvo_Level_With_Downloading.activate(self)

	def open_next_level(self):
		Basic_Philingvo_Level_With_Downloading.open_next_level(self)

	def prepare_output_params(self):
		self.params["set_length"] = self.set_length
		self.params[self.param_name] = self.item_class["slice_title"]
		self.params["slice_position"] = self.item_class["slice_position"]
		self.params["slice_length"] = self.item_class["slice_length"]

	def assign_item_language_for_pronunciation(self, item_class):
		Choosing_Level.assign_item_language_for_pronunciation(self, item_class)

class Choosing_Elements_Slice_Length(Choosing_Level):
	name = "elements in slice"
	main_color = "purple"
	param_name = "slice_length"
	item_position = 0
	next_level_class = Choosing_Slice_Number
	chunk_length = 5
	min_chunks = 2
	max_chunks = 6

	def __init__(self, *args, **kwargs):
		self.items = list(range(self.min_chunks*self.chunk_length,
								self.max_chunks*self.chunk_length,
								self.chunk_length))
		super().__init__(*args, **kwargs)

	def open(self, **kwargs):
		super().open(**kwargs)
		self.params["chunk_length"] = self.chunk_length

class All_Elements(Choosing_Slice_Number):
	name = "all elements in set"
	main_color = "lime"

class Slice_Of_Elements(Intermediary_Choosing_Level):
	name = "elements' slice"
	main_color = "pink"
	next_level_class = Choosing_Elements_Slice_Length

class Choosing_Elements_Length(Choosing_Level):
	name = "choose elements length"
	main_color = "red"
	param_name = "elements_length"
	items = [
			All_Elements,
			Slice_Of_Elements
			]

	def activate(self):
		next_level = self.item_class(self)
		self.open_level(next_level)

class Direct_Order(Level):
	name = "direct"
	main_color = "green"

class Reverse_Order(Level):
	name = "reverse"
	main_color = "red"

class Shuffle_Order(Level):
	name = "shuffle"
	main_color = "yellow"

class Choosing_Parts_Order(Choosing_Level):
	name = "parts order"
	main_color = "orange"
	param_name = "parts_order"
	items = [
			Direct_Order,
			Reverse_Order
			]
	next_level_class = Choosing_Elements_Length

class Choosing_Elements_Order(Choosing_Level):
	name = "elements order"
	main_color = "blue"
	param_name = "elements_order"
	items = [
			Direct_Order,
			Reverse_Order,
			Shuffle_Order
			]
	next_level_class = Choosing_Parts_Order

class Memorizing_Mode_Item(Level):
	name = "memorizing"
	main_color = "red"

class Revision_Mode_Item(Level):
	name = "revision"
	main_color = "blue"

class Choosing_Mode(Choosing_Level):
	name = param_name = "mode"
	main_color = "yellow"
	item_type_names = "modes"
	items = [
			Memorizing_Mode_Item,
			Revision_Mode_Item
			]
	next_level_class = Choosing_Elements_Order

class Assign_Params(Intermediary_Choosing_Level):
	name = "assign parameters"
	main_color = "yellow"
	next_level_class = Choosing_Mode

class Basic_Preset:
	mode = ["memorizing", "revision"]
	elements_order = ["direct", "reverse", "shuffle"]
	parts_order = ["direct", "reverse"]
	slice_length = "all"

class Params_Preset_Level(Level):
	chunk_length = 5
	chunks = 2
	mode = "revision"
	elements_order = "direct"
	parts_order = "direct"
	use_slice = False
	elements_text = "E"
	parts_text = "P"
	all_text = "all"
	slice_text = "slice"

	@property
	def slice_length(self):
		if self.use_slice:
			return self.chunk_length * self.chunks
		else:
			return "all"

	def get_name(self):
		if self.name:
			return self.name
		else:
			return "{mode} {slice} {e}-{elements_order} {p}-{parts_order}".format(mode=self.mode,
																				slice=self.slice_text if self.use_slice else self.all_text,
																				e=self.elements_text,
																				elements_order=self.elements_order[0],
																				p=self.parts_text,
																				parts_order=self.parts_order[0])

class Memorizing_Elements_Slice_In_Set_Direct_Direct(Params_Preset_Level):
	mode = "memorizing"	
	main_color = "yellow"

class Revision_All_Elements_In_Set_Direct_Direct(Params_Preset_Level):
	main_color = "green"

class Revision_All_Elements_In_Set_Shuffle_Direct(Params_Preset_Level):
	elements_order = "shuffle"

class Revision_All_Elements_In_Set_Direct_Reverse(Params_Preset_Level):
	parts_order = "reverse"

class Revision_All_Elements_In_Set_Shuffle_Reverse(Params_Preset_Level):
	elements_order = "shuffle"
	parts_order = "reverse"

class Revision_Elements_Slice_In_Set_Direct_Direct(Params_Preset_Level):
	use_slice = True

class Revision_Elements_Slice_In_Set_Shuffle_Direct(Params_Preset_Level):
	elements_order = "shuffle"
	use_slice = True

class Revision_Elements_Slice_In_Set_Direct_Reverse(Params_Preset_Level):
	parts_order = "reverse"
	use_slice = True

class Revision_Elements_Slice_In_Set_Shuffle_Reverse(Params_Preset_Level):
	elements_order = "shuffle"
	parts_order = "reverse"
	use_slice = True

class Memorizing_All_Elements_In_Set_Direct_Direct(Params_Preset_Level):
	mode = "memorizing"

class Choosing_Presets(Choosing_Level):
	name = "preset"
	main_color = "lime"
	items = [
			Memorizing_Elements_Slice_In_Set_Direct_Direct,
			Revision_All_Elements_In_Set_Direct_Direct,
			Revision_All_Elements_In_Set_Shuffle_Direct,
			Revision_All_Elements_In_Set_Direct_Reverse,
			Revision_All_Elements_In_Set_Shuffle_Reverse,
			Revision_Elements_Slice_In_Set_Direct_Direct,
			Revision_Elements_Slice_In_Set_Shuffle_Direct,
			Revision_Elements_Slice_In_Set_Direct_Reverse,
			Revision_Elements_Slice_In_Set_Shuffle_Reverse,
			Memorizing_All_Elements_In_Set_Direct_Direct
			]
	next_level_class = Choosing_Slice_Number
	
	item = None
	fields = ["name", "mode", "elements_order", "parts_order", "slice_length"]
	params_names = ["mode", "elements_order", "parts_order", "slice_length"]
	field_position = 0

	no_field_text_template = "No field {} text"

	def activate(self):
		self.copy_params_from_preset()
		super().activate()

	def copy_params_from_preset(self):
		for param_name in self.params_names:
			self.params[param_name] = self.item.__getattribute__(param_name)

	def show_first_item(self):
		self.item_position = 0
		self.show_level_name()

	def show_level_name(self):
		item_title_message = self.get_item_title()
		level_name_message = self.get_class_title(self.__class__)
		message = self.merge_messages(item_title_message, level_name_message, ": ")
		self.send_text_message(message)
	
	def get_item_title(self):
		if not self.item:
			self.item = self.get_item_class()(self)
		if len(self.fields) == 0:
			field_name = "name"
		else:
			field_name = self.fields[self.field_position]
			if field_name == "name":
				field_text = self.item.get_name()
			else:
				field_text = self.item.__getattribute__(field_name)
			field_name = field_name.replace("_", " ")
			if field_name == "name":
				field_name = "preset name"
			if field_text:
				text = "{} - {}".format(field_text, field_name)
			else:
				text = self.no_field_text_template.format(field_name)

		message_dict = self.interface.get_text_message(text)
		color = self.item.main_color
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

	def up(self):
		self.item = False
		super().up()

	def down(self):
		self.item = False
		super().down()

class Choose_Preset_With_Params(Intermediary_Choosing_Level):
	name = "choose preset with parameters"
	main_color = "lime"
	next_level_class = Choosing_Presets

class Choosing_Params_Source(Choosing_Level):
	name = param_name = "parameters source"
	main_color = "green"
	items = [
			Choose_Preset_With_Params,
			Assign_Params,
			]

	def activate(self):
		if len(self.items) > 0:
			item = self.item_class(self)
			item.open(**self.params)