#coding: utf-8

import vlc
from .basic_players import Player_Basic
from .sources import Philingvo_Dictionary_Source_Audio


class VLC_Philingvo_Dictionary_Audio_Player(Player_Basic):
	# VLC must be installed

	source_class = Philingvo_Dictionary_Source_Audio

	def get_request_url(self, **kwargs):
		return self.source.get_request_url(**kwargs)

	def __call__(self, **kwargs):
		request_url = self.get_request_url(**kwargs)
		if request_url:
			try:
				self.player = vlc.MediaPlayer(request_url)
				self.player.play()
			except Exception as error:
				return self.source.output_server_message_error(error)

	def pause(self):
		if self.player.is_playing():
			self.player.pause()
		else:
			self.player.play()

class VLC_Philingvo_Dictionary_Audio_With_Ballast_Player(VLC_Philingvo_Dictionary_Audio_Player):

	ballast_text = "the"

	def get_request_url(self, **kwargs):
		basic_request_url = super().get_request_url(**kwargs)
		return "{}%20{}".format(basic_request_url, self.ballast_text)