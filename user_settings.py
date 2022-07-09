#coding: utf-8

user_settings = {
"test_mode": False, # True - do not send messages to LED
"led_server_address": "192.168.0.123",
"led_server_address_port": 12345,
"show_command_messages_in_window": False,
"language": "en",
"auto_pronunciation": False,
"pronunciation_settings": {"pronunciation_player_name":
															# "gtts_stream", # Doesn't work
															"gtts_saving", # Works on Win
															# "pygame_philingvo_dictionary_audio_stream", # Streaming works for python 3.7.9 and pygame 1.9.4
															# "pygame_philingvo_dictionary_audio_saving", # Works on Win
															# "pygame_philingvo_dictionary_local_filepath", # Works on Win. Dictionary server and RUI must be run on the same machine
															# "vlc_philingvo_dictionary_stream", # Works on Win, VLC must be installed
															# "vlc_philingvo_dictionary_stream_with_ballast", # Works on Win # VLC must be installed

							"additional_player_settings": {"delete_audio_file_after": True,  # for players with saving
															"pronunciations_files_dir": "pronunciations", # for players with saving
															"philingvo_dictionary_pronunciation_server_address": "127.0.0.1:8050", # for players with philingvo dictionary 
															"play_random_pronunciation_file": False}
							},
"application_settings": {"philingvo_dictionary": {"address": "127.0.0.1:8050"}},
"window_settings": {"width": 800,
					"height": 300,
					"background_color": "black",
					"text_color": "red",
					"font_height": 36
					},
"letters_case_style": "upper", # upper, capitalize, title, lower, None - use styles of original spelling
# https://www.pygame.org/docs/ref/key.html
"keys": {"activate": "return",
		"up": "up",
		"down": "down",
		"left": "left",
		"right": "right",
		"main_menu": "home",
		"back": "backspace",
		"refrest_text": "f5",
		"pronounce": "space",
		"pronunciation_pause": ("p",),
		"close": "escape",
		}
}
