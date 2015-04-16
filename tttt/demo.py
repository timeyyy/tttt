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
#~ BSD 3-Clause License (Revised)
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.colorchooser import askcolor
import os
import sys

from tttt import TagManager
try:	
	from . import button_styling
except SystemError:
	import button_styling
'''
Demo Code for - Tims Tkinter Text Tags - https://github.com/timeyyy/tttt

search for '#tttt' to find places where the binding are used throught
the demo

On program run Automatically opens the file  'demo_xml_data' 
Saving will overide this file

Key binds are also enabled

pretty printed xml is saved in xml_on_load.txt and xml_on_save.txt
(for debugging purposes)

Command line option to load a document is also supported
python demo open_me.txt
'''

class MakerOptionMenu(tk.Frame):	#Used for creating Option Menus
	"""
	Subclass and define a start method
	
	Required Options include:
	
	self.options		-	elements in the drop down menu
	
	Optional settings:
	
	self.butnOptions = {'width':25,'direction':'below'}		- config
	self.heading		s-	heading item for the list
	self.initialValue	-	a heading that lasts until selection change
	self.auto_list_update 	- set to false to set updating list on click
		
	self.options can be either an iterable as well as a function
		
	To get results:
	use the self.var.get / set tkinter method
	or you can use:  def run_command(self, selection): 
	"""
	heading = None
	last_selected = ''	#internal value for decideding if the value had been updated or not
	auto_list_update = True
	frm_style = None
	def start(self):
		pass	#redifine lower
	def __init__ (self, parent =None,app=None):
		tk.Frame.__init__(self,parent)
		#~ self.config(takefocus=True)
		self.app = app
		self.parent=parent
		self.start()
		if self.frm_style==None:self.config(**cfg_guimaker_frame)
		else:self.config(**self.frm_style)
		if not hasattr(self,'initialValue'):
			self.initialValue='Select a Key'
		if self.conPack==None:self.pack(expand=1,fill='both')
		else:
			self.pack(**self.conPack)
		self.create_entries()		#creates self.LIST
		self.make_widget(self.LIST)		
	def make_widget(self,options):
		self.var=tk.StringVar()
		self.var.set(self.initialValue)
		if len(options)==0:options=['empty']
		self.wid=ttk.Menubutton(self,textvariable=self.var)
		if hasattr(self,'butnOptions'):self.wid.config(**self.butnOptions)
		self.wid.menu = tk.Menu(self.wid,tearoff=0)
		self.re_populate()
		self.last_selected = self.var.get()	#initalizing value
		self.wid.config(takefocus=True,menu=self.wid.menu)
		#~ self.wid.config(**self.butnConf)
		self.wid.pack(expand=1, fill='both')
		
	def create_entries(self):
		if self.heading == None:				# no heading
			if type(self.options)==list:self.LIST=self.options			# static list
			else:self.LIST=self.options()								#function that changes
		else: 									# with heading
			if type(self.options)==list:self.LIST=self.options[:]		# static list	
			else: 	self.LIST=self.options()							#function that changes														
			self.LIST.insert(0,self.heading)					

	def run_command(self, selection):             		# redefine me lower
		pass
	
	def get_result(self,value):	
		if self.auto_list_update:
			self.re_populate()
		self.run_command(value)
		self.var.set(value)		
	def re_populate(self):	
		self.create_entries()
		menu = self.wid.menu 
		menu.delete(0, 'end')								
		for string in self.LIST:	
			menu.add_command(label=string, 
							command=lambda value=string:
								 self.get_result(value))
###
#	SETTING UP TKINTER TEXT WIDGET
###
TITLE = "Vroom!"
DEFAULT_FILE = 'demo_xml_data' 
class RoomEditor(tk.Text):			#http://effbot.org/zone/vroom.htm  credits Fredrik Lundh
	def __init__(self, master, **options):
		tk.Text.__init__(self, master, **options)
		self.config(
			borderwidth=0,
			font=('Lucida Sans Typewriter', 12),
			foreground="green",
			background="black",
			insertbackground="white", # cursor
			selectforeground="green", # selection
			selectbackground="#008000",
			wrap=tk.WORD, # use word wrapping
			undo=True,
			#~ width=80,
			)
		self.tag_manager = TagManager(self)		#tttt
		self.filename = None # current document
		self.load('demo_xml_data')
	
	def _getfilename(self):			#Used for automaticly setting title
		return self._filename

	def _setfilename(self, filename):#Used for automaticly setting title
		self._filename = filename
		title = os.path.basename(filename or "(new document)")
		title = title + " - " + TITLE
		self.winfo_toplevel().title(title)

	filename = property(_getfilename, _setfilename)	

	def load(self,filename = None):
		if not filename:
			filename = askopenfilename(parent = self.master)
		data = open(filename).read()
		self.delete(1.0, tk.END)
		self.tag_manager.load_xml(data)				#tttt - this line replaces the code below
		#~ self.insert(tk.END, text)
		self.mark_set(tk.INSERT, 1.0)
		self.modified = False
		self.filename = filename

	def save_as(self, filename=None):
		if filename is None:
			filename = asksaveasfilename(parent = self.master)
		f = open(filename, "w")
		xml_text = self.tag_manager.save_with_xml()	#tttt - this line replaces the code below
		#text = editor.get(1.0, END)
		try:
			f.write(xml_text)
		finally:
			f.close()
		self.modified = False
		self.filename = filename
	
	def save(self):
		if not self.filename:
			filename = asksaveasfilename(parent = self.master)
			self.filename = filename
		f = open(self.filename, "w")
		xml_text = self.tag_manager.save_with_xml()	#tttt - this line replaces the code below
		#text = editor.get(1.0, END)
		try:
			f.write(xml_text)
		finally:
			f.close()
		self.modified = False
		
	def reload(self):		# For testing
		self.load(self.filename)
		
root = tk.Tk()
root.config(background="black")

editor = RoomEditor(root)			
editor.pack(fill='both', expand=1, pady=10)
editor.focus_set()

try:										# Load Command line args
	editor.load(sys.argv[1])
except (IndexError, IOError):
	pass

###
#	Style for ttk button styles for button state toggling
###
button_styling.install(root, imgdir='img')		

###
#	SETTING UP KEYBINDS
###
editor.bind('<Control-Key-b>', lambda e:editor.tag_manager.change_style('bold'))
editor.bind('<Control-Key-i>', lambda e:editor.tag_manager.change_style('italic'))
editor.bind('<Control-Key-u>', lambda e:editor.tag_manager.change_style('solid'))
editor.bind('<Control_L><o>', lambda e: editor.load())								# This bind syntax is different, the user has to release the keys before calling it again
editor.bind('<Control_L><s>', lambda e: editor.save())
editor.bind('<Control-Key-r>', lambda e: editor.reload())

###
#	SETTING UP BUTTONS AND CALLBACKS
###
tk.Button(root, text='load', command = lambda: editor.load()).pack(side ='right')
tk.Button(root, text='save', command = lambda: editor.save()).pack(side ='right')
tk.Button(root, text='reload', command = lambda: editor.reload()).pack(side ='right')

bold = ttk.Button(root, text='Bold', command = lambda: editor.tag_manager.change_style('bold'), style='ToggleButton')	#tttt
bold.pack(side='left')
italic = ttk.Button(root, text='Italic', command = lambda: editor.tag_manager.change_style('italic'), style='ToggleButton')	#tttt
italic.pack(side='left')
underline = ttk.Button(root, text='Underline', command = lambda: editor.tag_manager.change_style('solid'), style='ToggleButton')	#tttt
underline.pack(side='left')
overstrike = ttk.Button(root, text='Overstrike', command = lambda: editor.tag_manager.change_style('overstrike'), style='ToggleButton')	#tttt
overstrike.pack(side='left')
#~ colour = ttk.Button(root, text='Text Colour', command=lambda: change_colour('foreground'),style='ToggleButton') #tttt 
#~ colour.pack(side='left')
#~ highlighting = ttk.Button(root, text='Highlight Colour', command=lambda: change_colour('background')) #tttt 
#~ highlighting.pack(side='left')	
###
#	FONT SIZE AND FAMILY DROP DOWN LISTS, AlSO COLOUR CHOOSER
###
class FamilyMenu(MakerOptionMenu):	# Subclassing my gui builder and configuring
	def start(self):
		self.initialValue = 'Font'
		self.options = ['Arial','Times New Roman','Trebuchet Ms','Comis Sans Ms','Verdana','Georgia']
		self.conPack = {'expand':0,'side':'left'}
		self.frm_style = {'width':20}
	def run_command(self,value):
		editor.tag_manager.change_style(('family',value))	#tttt	
class SizeMenu(MakerOptionMenu):	#Subclassing my gui builder and configuring
	def start(self):
		self.initialValue = 'Size'
		self.options = [6,8,10,12,14,16,18]
		self.conPack = {'expand':0,'side':'left'}
		self.frm_style = {'width':20}
	def run_command(self,value):
		editor.tag_manager.change_style(('size',value))	#tttt				

class Colour(ttk.Button):
	def __init__(self, parent, colour_type):
		ttk.Button.__init__(self, parent)
		self.style = ttk.Style()
		self.style.configure('colour.TButton',background='red')
		self.config(command=lambda:self.change_colour(colour_type),
					width=8,
					style='colour.TButton')
		self.pack()
		#~ self.pack(expand=1,fill='both')
	def change_colour(self, colour_type):								# Colour type can be foreground or background
		value = askcolor()[1]
		editor.tag_manager.change_style((colour_type, value))
		self.style.configure('colour.TButton',background=value)
		
family_font_menu = FamilyMenu(root)							#initalize the menus
size_menu = SizeMenu(root)	
foreground = Colour(root, colour_type='foreground')
#~ background = Colour(root, colour_type='background')
###
#	SETTING UP BUTTON REFERENCES FOR INDENTING AND VALUE SETTING
###
editor.tag_manager.button_references = {'bold':bold,
										'italic':italic,
										'underline':underline,
										'family':family_font_menu.var,
										'overstrike':overstrike,
										'foreground':foreground,
										'size':size_menu.var
										} 
										#~ 'foreground':pass
def start():
	root.mainloop()
if __name__ == '__main__':
	print(help(TagManager))
	print(help(editor.tag_manager.change_style))
	start()			
