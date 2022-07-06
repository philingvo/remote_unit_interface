#coding: utf-8

from levels.basic_levels import Level
from .modes import Memorizing_Process_Mode
from .modes import Revision_Process_Mode


class Process(Level):
	name = "Activity Process Launcher"

	mode_classes = [Revision_Process_Mode,
					Memorizing_Process_Mode]

	no_mode_template = "There is no {} mode"

	def open(self, **kwargs):
		mode_name = kwargs["mode"]

		mode_class = self.get_mode_class(mode_name)
		if mode_class:
			process = mode_class(self)
			process.open(**kwargs)
		else:
			self.send_error_message(self.no_mode_template.format(mode_name))

	def get_mode_class(self, mode_name):
		for mode_classes in self.mode_classes:
			if mode_name == mode_classes.mode_name:
				return mode_classes
		return False

	def comeback(self):
		self.previous_level.comeback()