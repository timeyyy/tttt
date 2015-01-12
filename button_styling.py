#~ BSD 3-Clause License (Revised)
#~ 
#~ Copyright 2015 Timothy C Eichler (c) , All rights reserved.
#~ 
#~ Redistribution and use in source and binary forms, with or without modification, are 
#~ permitted provided that the following conditions are met:
#~ 
#~ 1. Redistributions of source code must retain the above copyright notice, this list of 
#~ conditions and the following disclaimer.
#~ 2. Redistributions in binary form must reproduce the above copyright notice, this list
#~ of conditions and the following disclaimer in the documentation and/or other materials 
#~ provided with the distribution. 
#~ 3. Neither the name of the nor the names of its contributors may be used to endorse or 
#~ promote products derived from this software without specific prior written permission. 
#~ 
#~ THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS 
#~ OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
#~ MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
#~ COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FORANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#~ EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE 
#~ GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED 
#~ AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILIT, OR TORT (INCLUDING 
#~ NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
#~ ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage
import os
import glob

colors = {
	#~ "frame": "#9ee874",	# a green color for testing etc 
	#~ "disabledfg": "#9ee874",
	#~ "selectbg": "#9ee874",
	#~ "selectfg": "#9ee874"
	"frame": "#efefef",
	"disabledfg": "#aaaaaa",
	"selectbg": "#657a9e",
	"selectfg": "#ffffff"
	}

imgs = {}
def _load_imgs(imgdir):			# Images without any references are garbage collected by python
	imgdir = os.path.expanduser(imgdir)
	if not os.path.isdir(imgdir):
		raise Exception("%r is not a directory, can't load images" % imgdir)
	for f in glob.glob("%s/*.gif" % imgdir):
		img = os.path.split(f)[1]
		name = img[:-4]
		imgs[name] = PhotoImage(name, file=f, format="gif89")

def install(root, imgdir):
	_load_imgs(imgdir)
	style=ttk.Style(root)
	
	ttk.Style().theme_create("toggle", "default", settings={
		#~ ".":		
		#~ {
			#~ "configure":
				#~ {"background": colors['frame'],
				 #~ "troughcolor": colors['frame'],
				 #~ "selectbackground": colors['selectbg'],
				 #~ "selectforeground": colors['selectfg'],
				 #~ "fieldbackground": colors['frame'],
				 #~ "font": "TkDefaultFont",
				 #~ "borderwidth": 1},
			#~ "map": {"foreground": [("disabled", colors['disabledfg'])]}
		#~ }, 
		
		"ToggleButton": {
			"configure": {"width": 10, "anchor": "center"},
			"layout": [
				("ToggleButton.button", {"children":
					[("ToggleButton.focus", {"children":
						[("ToggleButton.padding", {"children":
				[("ToggleButton.label", {"side": "left", "expand": 1})]
						})]
					})]
				})
			]
		},
		
		"ToggleButton.button": {"element create":
			("image", 'button-n',
		("pressed", 'button-p'), ("active","!alternate", 'button-h'),
				("alternate", "button-s"),	#THIS IS THE MAGIC tbutton-p
				{"border": [4, 10], "padding": 4, "sticky":"ewns"}
			)
		}
	}
	)
	
	style.theme_use('toggle')
	
	#~ style.configure('ToggleButton',foreground='red')
	
