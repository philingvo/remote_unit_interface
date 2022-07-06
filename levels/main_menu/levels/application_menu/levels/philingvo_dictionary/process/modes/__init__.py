from levels.basic_levels import Level
from levels.basic_levels import Quit_Menu
from ...final_activity_menu import Final_Activity_Menu
from ..activities import Basic_Activity
from ..activities import Memorizing_Activity
from ..activities import Revision_Activity

class Stop_Process(Quit_Menu):
	name = "stop activity process"
	# question_text_template = "Stop {}?"

	@property
	def question_text(self):
		return self.question_text_template.format(self.previous_level.mode_name)

class Basic_Process_Mode(Level):

	name = "activity process"
	mode_name = None
	activities_queue = []
	activities = []
	current_activity_position = 0
	current_activity = None
	additional_params_name = "additional_params"

	no_activities_template = "There aren't any activities in {} mode"

	def open(self, **kwargs):
		if len(self.activities_queue) >= 0:
			self.copy_input_params(kwargs)
			kwargs["mode_name"] = self.mode_name
			self.create_activities()
			self.open_activity(**kwargs)
		else:
			self.send_error_message(self.no_activities_template.format(self.mode_name))

	def copy_input_params(self, kwargs):
		self.params = kwargs

	def create_activities(self):
		self.activities = []
		for activity_position in range(len(self.activities_queue)):
			activity = self.activities_queue[activity_position]
			params = {}
			if isinstance(activity, list) and len(activity) > 1:
				activity_class = activity[0]
				activity_params = activity[1]
				if isinstance(activity_params, dict):
					params.update(activity_params)
			else:
				activity_class = activity
			
			if issubclass(activity_class, Basic_Activity):
				self.activities.append([activity_class(self), params])

	def get_current_activity(self):
		if len(self.activities) >= 0:
			return self.activities[self.current_activity_position]
		else:
			return False

	def open_activity(self, **kwargs):
		current_activity = self.get_current_activity()
		if current_activity:
			if kwargs.get(self.additional_params_name):
				del kwargs[self.additional_params_name]
			additional_activity_params = current_activity[1]
			if len(additional_activity_params) > 0:
				kwargs[self.additional_params_name] = additional_activity_params
			current_activity[0].open(**kwargs)

	def next_activity(self, **kwargs):
		self.current_activity_position += 1
		if self.current_activity_position < len(self.activities):
			self.open_activity(**kwargs)

	def previous_activity(self, **kwargs):
		self.current_activity_position -= 1
		if self.current_activity_position >= 0:
			self.open_activity(**kwargs)

	@property
	def is_last_activity_position(self):
		return self.current_activity_position == len(self.activities) - 1

	@property
	def is_first_activity_position(self):
		return self.current_activity_position == 0

	def comeback(self):
		quit_menu = Stop_Process(self)
		quit_menu.open()

	def escape(self):
		self.previous_level.comeback()

	def resume(self):
		current_activity = self.get_current_activity()
		current_activity[0].reopen()

	def repeat(self):
		for activity in self.activities:
			activity[0].set_start_positions()
		
		self.current_activity_position = 0
		self.resume()

	def reopen_activity_last_step(self):
		current_activity = self.get_current_activity()
		current_activity[0].reopen_last_step()

	def reopen_activity_and_show_info_field_item(self):
		current_activity = self.get_current_activity()
		current_activity[0].reopen_and_show_info_field_item()

	def open_final_activity_menu(self):
		print('OPEN FINAL MENU', self.name)
		return_menu = Final_Activity_Menu(self)
		return_menu.open(**self.params)

class Memorizing_Process_Mode(Basic_Process_Mode):
	mode_name = "memorizing"
	activities_queue = [
						Memorizing_Activity,
						[Revision_Activity, {"attempts": 1}],
						# [Revision_Activity, {"attempts": 2}],
						# [Revision_Activity, {"elements_order": "shuffle"}],
						# [Revision_Activity, {"attempts": 2, "parts_order": "reverse"}],
						# [Revision_Activity, {"elements_order": "reverse"}],
						]

class Revision_Process_Mode(Basic_Process_Mode):
	mode_name = "revision"
	activities_queue = [Revision_Activity]