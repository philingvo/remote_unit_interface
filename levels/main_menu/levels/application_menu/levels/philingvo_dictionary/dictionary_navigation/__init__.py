#coding: utf-8

from ..basic_levels import Basic_Philingvo_Level_With_Downloading
from ..choosing_params import Choosing_Params_Source


class Sets(Basic_Philingvo_Level_With_Downloading):

	name = path = downloading_target = item_type_names = "sets"
	query_string_path = "topic_id"
	fields = [["id"],
			"position",
			["title"],
			["type", "name"],
			["type", "language", "original_name"],
			["abstract"],
			["created_at"]]
	language_code_path = ["type", "language", "code"]
	field_position = 2
	main_container_field = param_name = "set"
	next_level_class = Choosing_Params_Source

	def prepare_output_params(self):
		super().prepare_output_params()
		self.params["set_id"] = self.params["item_id"]
		del self.params["item_id"]

class Topics(Basic_Philingvo_Level_With_Downloading):

	name = path = downloading_target = item_type_names = "topics"
	query_string_path = "subject_id"
	fields = [["id"],
			"position",
			["title"],
			["language", "original_name"],
			["abstract"],
			["created_at"]]
	language_code_path = ["language", "code"]
	field_position = 2
	main_container_field = param_name = "topic"
	next_level_class = Sets

class Subjects(Basic_Philingvo_Level_With_Downloading):

	name = path = downloading_target = item_type_names = item_type_names = "subjects"
	query_string_value = False
	fields = ["id",
			"position",
			"title",
			["language", "original_name"],
			"abstract",
			"created_at"]
	language_code_path = ["language", "code"]
	field_position = 2
	main_color = "red"
	param_name = "subject"
	next_level_class = Topics

class Sets_In_Playlist(Sets):

	name = downloading_target = "sets in playlist"
	path = "sets_in_playlist"
	query_string_path = "playlist_id"

class Playlists(Basic_Philingvo_Level_With_Downloading):

	name = path = downloading_target = item_type_names = "playlists"
	query_string_value = False
	fields = ["id",
			"position",
			"title",
			["language", "original_name"],
			"abstract",
			"created_at"]
	language_code_path = ["language", "code"]
	field_position = 2
	main_color = "green"
	param_name = "playlist"
	next_level_class = Sets_In_Playlist