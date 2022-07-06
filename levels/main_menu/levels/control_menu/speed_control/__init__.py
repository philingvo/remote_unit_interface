#coding: utf-8

from levels.basic_levels import Level
from levels.basic_levels import Command


class Speed_Up_Command(Command):
	name = "Speed Up"
	main_color = "green"
	command = "speed_up"

class Slow_Down_Command(Command):
	name = "Slow Down"
	main_color = "red"
	command = "slow_up"

class Set_Delay_Time(Level):
	name = "Set Delay Time"
	main_color = "yellow"
	command = 'set_delay_time'
	value = False
	default_value = 0.05
	min_value = 0
	max_value = 2
	step = 0.01

	abstract_text = "Push ENTER to submit delay time. Push UP to increase (slower). Push DOWN to decrease (faster)"
	abstract_text_styles = {"main_color":"yellow",
							"letters_colors":{"main_color":{"red":["5-9"],"blue":["38-39"],"green":["68-71"]}}} # WORKS ONLY FOR ENGLISH
	current_delay_value_text_template = "Delay is {} seconds"
	maximum_adjective_text = "max"
	minimum_adjective_text = "min"
	submit_text_template = "{} seconds. Push ENTER to submit delay time"
	warning_message_text_template = "{} seconds is {}!"

	@classmethod
	def change_name(self, value):
		self.default_value = value

	def open(self):
		if not self.value:
			self.set_level()
			message = self.interface.get_colored_text_message(self.abstract_text, **self.abstract_text_styles)
			self.value = self.default_value
		else:
			message = self.current_delay_value_text_template.format(self.rounded_value)
			self.set_value()
		self.send_text_message(message)

	def activate(self):
		self.open()

	def up(self):
		if self.value:
			self.value += self.step
			if self.value <= self.max_value:
				message = self.get_value_message('blue')
			else:
				self.value -= self.step
				message = self.get_warning_message(self.maximum_adjective_text)
			self.send_text_message(message)

	def down(self):
		if self.value:
			self.value -= self.step
			if self.value >= self.min_value:
				message = self.get_value_message('green')
			else:
				self.value += self.step
				message = self.get_warning_message(self.minimum_adjective_text)
			self.send_text_message(message)

	def get_value_message(self, color):
		submit_text = self.submit_text_template.format(self.rounded_value)
		letters_indexes_rage = (19, 23) if self.rounded_value // 0.1 == 0 else (18, 22)
		submit_text_styles = {"main_color": color,
							"letters_colors":{"main_color":{"red":["-".join(map(str, letters_indexes_rage))]}}}
		return self.interface.get_colored_text_message(submit_text, **submit_text_styles)

	def get_warning_message(self, adjective):
		return self.interface.get_error_message(self.warning_message_text_template.format(self.rounded_value, adjective))

	@property
	def rounded_value(self):
		return round(self.value, 2)

	def set_value(self):
		self.interface.send_command({"command": self.command,
									"value": self.rounded_value})

class Speed_Control_Menu(Level):
	name = "Speed Control Commands"
	main_color = "yellow"
	items = [
			Speed_Up_Command,
			Slow_Down_Command,
			Set_Delay_Time
			]
	changeable_items = [
						Set_Delay_Time
						]