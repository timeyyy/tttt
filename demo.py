from tttt import XmlManager
import tkinter as tk
import tkinter.ttk as ttk
import os, sys
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
#~ sys.path.append(os.path.join(os.getcwd(),'tttt'))

'''
Demo Code for - Tims Tkinter Text Tags - https://github.com/timeyyy/tttt

search for '#tttt' to find places where the binding are used throught
the demo

On Open Automatically opens the file  'demo_xml_data' 

Key binds are also enabled

pretty printed xml is saved in xml_on_load.txt and xml_on_save.txt
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
	
	def get_result(self,value):	#get result after change, this is default method done by polling the list
		if self.auto_list_update:
			self.re_populate()
		self.run_command(value)
		self.var.set(value)		#TBD ISSUE1 this needs to be uncommented on windows, but i think on linux not dbl check!
	def re_populate(self):	#http://stackoverflow.com/questions/19794069/tkinter-gui-update-choices-of-an-option-menu-depending-on-a-choice-from-another
		self.create_entries()	#recreates the self.LIST value
		#~ menu = self.wid['menu'] #menu
		menu = self.wid.menu #menu
		menu.delete(0, 'end')		#delete all						
		for string in self.LIST:	#recreate list
			menu.add_command(label=string, 
							command=lambda value=string:
								 self.get_result(value))

TITLE = "Vroom!"
DEFAULT_FILE = 'demo_xml_data' 
class RoomEditor(tk.Text):			#http://effbot.org/zone/vroom.htm  credits Fredrik Lundh
	def __init__(self, master, **options):
		tk.Text.__init__(self, master, **options)
		
		self.config(
			borderwidth=0,
			font="{Lucida Sans Typewriter} 14",
			foreground="green",
			background="black",
			insertbackground="white", # cursor
			selectforeground="green", # selection
			selectbackground="#008000",
			wrap=tk.WORD, # use word wrapping
			undo=True,
			width=64,
			)
		
		self.tag_manager = XmlManager(self)		#tttt
		self.filename = None # current document
		self.load('demo_xml_data')
	
	def _getfilename(self):			#Used for automaticly setting title
		return self._filename

	def _setfilename(self, filename):#Used for automaticly setting title
		self._filename = filename
		title = os.path.basename(filename or "(new document)")
		title = title + " - " + TITLE
		self.winfo_toplevel().title(title)

	filename = property(_getfilename, _setfilename)	#Used for automaticly setting title

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
		

root = tk.Tk()
root.config(background="black")

editor = RoomEditor(root)			
editor.pack(fill=tk.Y, expand=1, pady=10)

editor.focus_set()

try:
	editor.load(sys.argv[1])
except (IndexError, IOError):
	pass


#line count
#tag_manager.line_count()

editor.bind('<Control_L><b>', lambda e:editor.tag_manager.change_style('bold'))
editor.bind('<Control_L><i>', lambda e:editor.tag_manager.change_style('italic'))
editor.bind('<Control_L><u>', lambda e:editor.tag_manager.change_style('solid'))
editor.bind('<Control_L><o>', lambda e: editor.load())
editor.bind('<Control_L><s>', lambda e: editor.save())

tk.Button(root, text='load', command = lambda: editor.load()).pack(side ='right')
tk.Button(root, text='save', command = lambda: editor.save()).pack(side ='right')
bold = tk.Button(root, text='Bold', command = lambda: editor.tag_manager.change_style('bold'))	#tttt
bold.pack(side='left')
italic = tk.Button(root, text='Italic', command = lambda: editor.tag_manager.change_style('italic'))	#tttt
italic.pack(side='left')
underline = tk.Button(root, text='Underline', command = lambda: editor.tag_manager.change_style('solid'))	#tttt
underline.pack(side='left')
overstrike = tk.Button(root, text='Overstrike', command = lambda: editor.tag_manager.change_style('overstrike'))	#tttt
overstrike.pack(side='left')

class family_menu(MakerOptionMenu):	#Subclassing my gui builder and configuring
		def start(self):
			self.initialValue = 'Font'
			self.options = ['Arial','Times New Roman','Trebuchet Ms','Comis Sans Ms','Verdana','Georgia']
			self.conPack = {'expand':0,'side':'left'}
			self.frm_style = {'width':20}
		def run_command(self,value):
			editor.tag_manager.change_style(('family',value))	#tttt	
class size_menu(MakerOptionMenu):	#Subclassing my gui builder and configuring
		def start(self):
			self.initialValue = 'Size'
			self.options = [6,8,10,12,14,16,18]
			self.conPack = {'expand':0,'side':'left'}
			self.frm_style = {'width':20}
		def run_command(self,value):
			editor.tag_manager.change_style(('size',value))	#tttt	

family_menu(root)							#initalize the menus
size_menu(root)	

#button references
editor.tag_manager.button_references = {'bold':bold,
										'italic':italic,
										'underline':underline} 
print(help(editor.tag_manager.change_style))
root.mainloop()
