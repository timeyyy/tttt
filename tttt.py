# - been playing with defaults gui.. need the button style to indent on click
	#http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/ttk-map.html
	#also been working with this in gui archetypes in the on_bold func

'''
----Overview----

Behavour of adding and removing tags is modeled on libre office

Hanldes changes when the text is selected or the 
cursor is in a word	 
when typing uses the style of previous char
If a style is changed at the end or start of a word
When the user types it will have that new setting
if the user clicks away the setting is read from the new position
'''

	
'''
Thoughts
So when entering data must decide if to overide or not
On mouse click in text widget must decide to show button states or not

On Change style have to also change button state

To Change button state i need a reference to the button!
-button references get saved when init called, 
-then i use the references in functions to set values

''' 

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font
import xml.etree.ElementTree as ET
from timstools import DPRINT, InMemoryWriter, ignored, toggle
import functools
import logging
import sys, time, xml.dom.minidom # nur  zum testen http://stackoverflow.com/questions/749796/pretty-printing-xml-in-python
#~ print(help(ET.Element.getiterator))
namespaces = {'office': 'www.what.com','style':'www.style.com'}
#~ root = self.tree.getroot()		#unavalibel when pasrse from str, .. bug in element tree
class MixInText:
	"""
	General Mix in methods for tkinter Text widget
	"""
	def word_at_index(self,cursor):
		'''Returns start and indexs of a word at given cursor position'''
		text = self.text
		if text.get(cursor) in (' ','\n'):				#right extremity of the word
			end = cursor
		elif cursor == text.index('end-1c'):	#if at end of text widget, end is alwas with new line so move one back
			end = cursor
		else:
			holder = cursor+'+1c'
			for i in range(0,9999999999999999):
				if text.get(holder) in (' ','\n'):
					end = holder
					break
				elif str(holder).split('+')[0] == text.index('end-1c'):	#the str looks like 1.0+1c+1c etc
					end = holder										
					break
				else:
					holder = holder +'+1c'
					
		holder = cursor	
		if text.get(holder+'-1c') == '\n':	#left extremity of the word
			start = cursor
			#~ print('FOUD START GIVEN',start)
		elif text.index(cursor) == '1.0':	#if at pos 1.0
			start = cursor
		else:
			holder = holder +'-1c'
			for i in range(0,9999999999999999):
				#~ print(text.index(holder))
				if text.get(holder) in (' ','\n'):
					start = holder+'+1c'
					break
				elif text.index(holder) == '1.0':
					start = holder
					break
				else:
					holder = holder +'-1c'
		word = text.get(start,end)
		return word, text.index(start), text.index(end), len(word)
			
	def text_from_tag(self, tag):	
		'''returns the start index, and text for each instance of
		a tag'''
		zipped = zip(self.text.tag_ranges(tag)[0::2], self.text.tag_ranges(tag)[1::2]) #the second pareametr of slice is a step #http://stackoverflow.com/questions/4647050/collect-every-pair-of-elements-from-a-list-into-tuples-in-python
		for start, end in zipped:	#for each section that has the tag,
			#~ print('start and end TEXT_from_Tag : %s,  %s '% (start,end))
			yield start, self.text.get(start,end)

	@staticmethod
	def button_state_toggle(but):
		if toggle(but):
			print(1)
			but.config(default='active')
		else:
			print(2)
			but.config(default='normal')		
	
	@staticmethod
	def button_state_change(but,state):	#in cases wher i want to change values but based on a variable not simple toggle
		'''
		Used for setting buttons as selected or unselected.
		
		To see how to create the style of the selected state see below.
		
		str 'toggle' to toggle from the current state
		1 to set default to active 		-Pressed state
		0 to set default state to normal
		
		tkinter.ttk.Style().theme_create("toggle", "default", settings={
		".": 
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
		}
		
		"ToggleButton.button": {"element create":
			("image", 'button-n',
		("pressed", 'button-p'), ("active","!alternate", 'button-h'),
				("alternate", "button-s"),#THIS IS THE MAGIC tbutton-p
				{"border": [4, 10], "padding": 4, "sticky":"ewns"}
			)
		}
		

		'''
		if state == 'toggle':
			print('Value of cet : ',but.cget('default'))
			if str(but.cget('default')) == 'normal': #button state not pressed
				print('set to active')
				but.config(default='active')
			else:
				but.config(default='normal')
		elif state:
			print(1)
			but.config(default='active')
		else:
			print(2)
			but.config(default='normal')
	
	
	def default_tag(self, event):	#controlls binding tags on insert,
		"""
		text.bind('<Key>',lambda e: default_tag(e))
		"""
		def let_update_add_tag(index):					#fuck, tried using after method before function call but it wasnt working
			print('LET ME UPDATE')
			print(' text: ',text.get(index))
			print('index',index)
			print('tag to be added',current_tag)
			text.tag_add(current_tag,index)
			print(current_tags,'current tags')
			print(char_before,'char before')
			#~ current_tags = self.text.tag_names(index)
			#~ current_tag = current_tags[-1]
			#~ print(self.text.get(cursor+'1c'),'gotten text')
			#~ print(current_tags,'current tags')
			print('len current tags,',len(current_tags))
			if current_tags[0] != current_tag:			#remove old tag
				text.tag_remove(current_tags[0],index)
			print('fin defualt tag')
			print()
		text = event.widget																																								
		#~ last = text.index('insert')
		#~ print('cursor pos',last)
		#~ print(last,text.index('insert'))
		#~ row, col = last.split('.')
		if event.char is not '' and len(repr(event.char)) >= 3:	#no blank chars from special charachters, the and statement with > blocks keys such as ctrl + (something)
			#~ print(len(repr(event.char)))
			#~ print('I AM A  CHAR WHAT ',event.char,type(event.char),repr(event.char))
			cursor = text.index('insert')
			char_before = text.index(cursor + '-1c')	#1 char less    						
			current_tags = text.tag_names(char_before)		#which tag does the char before have?    						
			print('index before and char',char_before,text.get(char_before))
			print('current tags at char before',current_tags)
			print('insert index and text',cursor,text.get(cursor))
			print('current tags at insert',text.tag_names(cursor))
			try:
				current_tag = current_tags[-1]			#tag
			except IndexError:	#if there is no tag already then add the default should run 1t pos 1.0 only
				print('adding the default tag.. index error')
				current_tag = 'default'
			print('current tag before if and elif',current_tag)
			row, col = cursor.split('.')
			if self.overide_state:						#a value is being saved here to overide the defualt behavior
				print('using overide state',self.overide_state)
				current_tag = self.overide_state
			elif col == '0' and row != '1':#if at start of row, and text exists to the right of the cursor take that style
				print('COL WAS ZERO')
				def let_text_get():
					print(text.index(cursor),text.get(cursor),text.get(cursor+'+1c')=='\n')
					if text.get(cursor+'+1c') != '\n':	#data exists after the cursour, so take that setting
						print(text.index(cursor))
						current_tags = text.tag_names(cursor+'+1c')
					else:								#get style from last line, which is default behavior
						print('get style from last line, aka default behaviuor one char back')
						current_tags = text.tag_names(cursor+'-1c')
					current_tag = current_tags[-1]
					print(current_tag)
					text.tag_add(current_tag,cursor)
					if current_tags[0] != current_tag:			#remove old tag
						text.tag_remove(current_tags[0],cursor)
				text.after(1,let_text_get)
				return
			print(current_tag,' < - Tag to Be added')
				
			text.after(1,functools.partial(let_update_add_tag,cursor))
			self.overide_state = 0	#back to default behavior
			time.sleep(0.1)

	def check_button_state(self, event): #on mouse over 
		'''
		uncheck all buttons
		check if text before cursour has settings
		then set the buttons to those values for lists or alternate style for buttons
		 
		'''
		cursor = self.text.index('insert')

		print('-----------Checking Button States---- on mouse focus')
		print('Cursor position :',cursor)
		print('All tags at cursor',self.text.tag_names(cursor))
		with ignored(IndexError):
			current_tag = self.text.tag_names(cursor)[-1]
			print('All attributes in last tag',self.styles[current_tag])
		#Checking style at cursor, do buttons need to be indented?
		
		with ignored(KeyError,AttributeError):			#incase no button defined for that styyle option, and if no button references defined
			for attrib,button in self.button_references.items(): # 				Turning all button states off
				if button not in ('family','size'): #these have no off state 0.o
					#~ print('DEPRESSING: ',attrib)
					self.button_state_change(self.button_references[attrib],(0))
		
		with ignored(IndexError):  	#Turning on Buttons 
			current_char = self.text.get(cursor)
			if current_char in (' ','\n'):		#handles being at end of a word
				cursor = cursor+'-1c'
			current_tag = self.text.tag_names(cursor)[-1]	
			for attribute in self.styles[current_tag]:	
				if type(attribute) == tuple:	#so far size and font family are passed in as tuples
					attribute = attribute[0]	
				with ignored(KeyError,AttributeError):			#incase no button defined for that style option
					self.button_state_change(self.button_references[attribute],(1)) # press it
					#~ print('PRESSING :',attribute)

class XmlManager(MixInText):		# Xml handling class for loading and saving, changing tags into xml
		option_list = {'bold':{'weight':'bold'},'solid':{'underline':1},'italic':{'slant':'italic'},
		'overstrike':{'overstrike':1}}
		styles = {'default':[]}	#so when all tags are removed this default will get loaded, on init the users settings get made into the corresponding tag
		"""
		
		run tk_text_xml.py as a script for a demo
		
		the behaviour of adding tags was modelled from libre office


	
		Allows multiple tags for customizing a text widget to be saved
		and loaded as xml
		
		Supported Data format at the moment is only as a string
		
		Supports all tags of Text widget, see change_style for more info
		
		to change the default text type do this
		
		my_text_xml.custom_default_style = [
		'bold','sold','italic',('family',arial),('size',15)]
		
		-----Short Example-----
		
		my_text_xml = XmlManager(TextWidget):
			
		###load data from database etc
		
		my_text_xml.load_xml(data)
		
		###save your data
		
		data = my_text_xml.save_with_xml()
		
		###Add or Remove a property (based on the first character)
		
		my_text_xml.change_style(required change here)
		see change_style help for more info
		
		"""
		def __init__(self, text):

			self.text = text	
			self.text.bind('<Key>',lambda e: self.default_tag(e))	#applies a default tag on insert, so we know which elements have no tags, this will be removed on adding another tag
			self.text.bind('<Button-1>',lambda e: self.text.after(1,functools.partial(self.check_button_state,e)))	#check if text at insertion point has bold italic or underline tags, then set buttons to alternative style		
			self.overide_state 		= 0		#if the state is active it will overide the default behabvior of style grabbing	
			#~ self.load_style_tags()		#Load defaults and anyother tags present. TBD, load file controller seems to be propogating the load ? i would like to check that and see if it is a good idea or not to load when the page is first created
			self.custom_default_style = 0   # TBD implement, see help above
		def load_xml(self,data):	#data here is a str of xml
			'''
			pass in xml data that has been previously saved 
			to load it as normal text
			'''
			print('starting load')
			#~ print(data)
			
			if data.strip():										#Peparing to pretty print for debug
				xmlt = xml.dom.minidom.parseString(data)		
				pretty_xml_as_string = xmlt.toprettyxml()
				with open('xml_on_load.txt','w') as f:			#This file is written for debug purposes
					f.write(pretty_xml_as_string)
				
			with ignored(ET.ParseError):					#if parse error i.e no xml tags, just pass
				tree = ET.fromstring(data)					#create xml tree from str	
				auto_styles = tree.find('automatic-styles')	
				body = tree.find('body')
				for style in auto_styles:						#Recreating Style Options
					key = style.get('name')
					values = []
					text_properties = style.find('text-properties')
					weight			= text_properties.get('weight')		
					font_style 		= text_properties.get('font-style')	#italic
					underline_style = text_properties.get('text-underline-style')
					font_size		= ('size',text_properties.get('font-size'))
					bg				= ('background',text_properties.get('background-color'))	#TBD TEST  COLOR OPTIONS 
					fg				= ('foreground',text_properties.get('color'))	#font color
					font_name		= ('family',text_properties.get('font-name'))	#family e.g arial
					over			= text_properties.get('text-line-through-type')	#overstrike
					
					values = [weight,font_style,underline_style,font_size,font_name,bg,fg,over]	#add all items and remove the null values
					filtered = []	
					for item in values:	#filter the none values out of the tupled and normal items
						try:
							if item[1] is not None:			#some values are passed in as a tuple and have to be handled differently
								filtered.append(item)
						except TypeError:
							if item is not None:
								filtered.append(item)
					self.styles[key] = filtered				#add to styles dictionary
			
			DPRINT(self.styles.items(),'succesfully recreated styles')
			self.load_style_tags()		#loading the styles into text tags 
			
			#Inserting text into widget
			with ignored(UnboundLocalError):	#this with handles case of no body tag i.e first creation
				body_iter = body.getiterator()	
				body_iter.__next__()			#skip the body tag itself
				for xml_tag in body_iter:	
					#~ DPRINT(xml_tag.text,'TAG = %s' % xml_tag.get('style-name'))
					original_index = self.text.index('insert')	# position moves after text is inserted so save it now			
					self.text.insert('insert',xml_tag.text)								#text inserted
					ending_index = self.text.index('end -1c')	#new lines are saved when text data is gotten so move back 2 characters
					self.text.tag_add(xml_tag.get('style-name'),original_index,ending_index)	#tag added
					#~ print(repr(xml_tag.text),'repr')
					#~ DPRINT(self.text.get(original_index,'end'),'TEXT FROM INDEX: %s to %s' % (original_index,ending_index))
				#~ print(self.text.tag_ranges('default'),'def')
				#~ print(self.text.tag_ranges('p1'),'p1')
			print('FINISHED LOADING')
		
		def load_style_tags(self):	#loading the styles into text tags 
			print('loading the styles into text tags')
			for name, style in self.styles.items():
				new_font = tkinter.font.Font(self.text, self.text.cget("font"))	#???
				for item in style:								# configure font attributes 
					print('the item in style is :',item)
					try:
						new_font.configure(**self.option_list[item])	#option_list contains the option name for the setting
					except KeyError:							#some values are passed in as tuple so handle differently
						print(item, 'configured item')
						if item[0] == 'size':			#http://effbot.org/tkinterbook/tkinter-widget-styling.htm
							new_font.configure(size = item[1])
						if item[0] == 'family':
							new_font.configure(family = item[1])
						if item[0] == 'background':
							new_font.configure(background = item[1])
						if item[0] == 'foreground':
							new_font.configure(foreground = item[1])
				self.text.tag_configure(name, font=new_font)	#add tag to font
				#~ print('TAG NAMES LOADED')
				print(self.text.tag_names())
		def save_with_xml(self): # a controller type function
			"""
			Returns all data from the text widget formatted with xml
			Store as you please
			
			data = my_xml_text.save_with_xml()
			"""
			data = self.text.get('1.0', tk.END+'-1c') 
			print('Starting save')
			self.xml_setup()
			self.convert_text_to_xml(data)		#data is saved in the tree
			xml_data = self.save_style_info()	#saves tags into automatic-styles xml tag and returns data
			
			xmlt = xml.dom.minidom.parseString(xml_data)	#This code block is for debugging purposes
			pretty_xml_as_string = xmlt.toprettyxml()
			with open('xml_on_save.txt','w') as f:
				f.write(pretty_xml_as_string)
				
			return xml_data						#user will decide how to save the str
		
		def xml_setup(self):							#create standard xml template
			root = ET.Element("document-content")					
			auto_styles = ET.SubElement(root, "automatic-styles")
			body = ET.SubElement(root, "body")
			tree = ET.ElementTree(root)					#wrap it in an ElementTree instance
			self.tree = tree				
		def convert_text_to_xml(self,new_data):			
			#~ Search for range of tag
			#~ get the text at that point
			#~ add text to dict with key as start pos
			#~ repeat
			#~ order and xml

			holder = {}		#TBDTBDTBD Properly name
			body = self.tree.find('body')					#navigate to body				
			for tag in self.styles.keys():						#for all ranges of a tag, 
				for start, text in self.text_from_tag(tag):
					holder[str(start)] = [tag, text]			# ADD TEXT TO DICT WITH KEY AS POS
					#~ print(repr(text),'data')
			print('sorting it by positions and creating xml tags')
			#~ print(holder)
			for i, pos in enumerate(sorted(holder.keys())):	#sorting text by positions and creating xml tags
				row, col = pos.split('.')
				row, col = int(row), int(col)
				tag_name, text = holder[pos]				#text to be inserted
				tag_type = tag_name							#needs to be differentiated from the tag_name
				
				if tag_type[0] == 'T':	#change to a span tag TBD 
					tag_type = 'span'
				else:
					tag_type = 'p'		# p type tag
				XML_tag = ET.SubElement(body, tag_type)		#tag 
				XML_tag.set('style-name', tag_name)			#style name
				XML_tag.text = text	
	
		def save_style_info(self):	# saves the style info in automatic styles xml tag info
			auto_styles = self.tree.find('automatic-styles')
			for key, values in self.styles.items():
				xml_tag = ET.SubElement(auto_styles, 'style')
				xml_tag.set('name', key)
				text_properties = ET.SubElement(xml_tag, 'text-properties')
				if 'solid' in values: 
					text_properties.set('text-underline-style', 'solid')	
				if 'bold' in values:
					text_properties.set('weight', 'bold')
				if 'italic' in values:
					text_properties.set('font-style', 'italic')
				if 'overstrike' in values:
					text_properties.set('text-line-through-type', 'single')
				with ignored(IndexError):
					for setting in values:
						if setting[0] =='size':
							text_properties.set('font-size', str(setting[1]))
						elif setting[0] =='family':
							text_properties.set('font-name', setting[1])
						elif setting[0] =='background':
							text_properties.set('background-color', setting[1])
						elif setting[0] =='foreground':
							text_properties.set('color', setting[1])
			
			mw = InMemoryWriter()	#acts as a file but saves in memory
			self.tree.write(mw)		#our xml tree is written to our memory file
			return mw.data[0].decode('utf-8')	#mw.data contains the written data

		def change_style(self,requested_change):
			'''
			Pass in desired style change
			supports the following:
			
			bold, italic, underline, overstrike
			
			send in size as an interger 	('size',value)
			send in a font name as 			('family',value)
			'''
			
			#~ if requested_change == 'underline': requested_change = 'solid' #much better to call underline not solid, mapping for convienecne
			#button ref requires it to be solid though ö
			try:														
				print()
				cursor = self.text.index('insert')
				self.change_style_selected(requested_change)	#handle selected text
				self.text.mark_set('insert',cursor)				#restore cursor position
				
			except(tk.TclError) as e:
				if not 'sel' in str(e):							#catching only desired error
					print('unexpected error ')
					raise e
					sys.exit()
				else:											#if no selected text
					self.change_style_non_select(requested_change)
					self.text.focus_force()							#refocuses after clickng on button	
							
		def change_style_selected(self,requested_change): # what to do on selected text
			current_tags = self.text.tag_names('sel.first')		#all tags on the first charcher	     
			current_tag = current_tags[-1]						#last added tag	
			#~ DPRINT([current_tag,requested_change,self.styles],'cur tag req change and styles list')
			#~ print(current_tags)
			with ignored(KeyError,AttributeError):		# if a references for a button is not set and the variable isnt configure
				button = self.button_references[requested_change]	#reference for depressing or pressing button in
			if current_tag == 'sel' or requested_change not in self.styles[current_tag]: #ADD request
				#~ print('add request@ %s , %s' % (self.text.index('sel.first'),self.text.index('sel.last')))
				#~ self.button_state_change(button,1)		#press button
				style = self.check_styles(requested_change,current_tag,remove=False)
				self.text.tag_remove(current_tags[1],'sel.first','sel.last')	#removing old tag
			else:																		#REMOVE request
				#~ print('remove request @ %s , %s' % (self.text.index('sel.first'),self.text.index('sel.last')))
				#~ self.button_state_change(button,0)		#depress button
				style = self.check_styles(requested_change,current_tag,remove=True)			
				#~ self.text.tag_add('default','sel.first','sel.last')				#adding default tag
			
			#~ DPRINT(style,'style after check')											
			if type(style) is str:								#style is the key of the style (already created)
				#~ print(style,'using this already created style')
				self.text.tag_add(style, "sel.first", "sel.last")
				self.text.tag_remove(current_tag, "sel.first", "sel.last")
				
			elif not style:						#len is  0 , so we had a tag removed, so load default style
												# i think this was toi handle sel but now im using default method tihs is mute point, mod check_style to remove errenoruse checks
				self.text.tag_remove(current_tag, "sel.first", "sel.last")
			else:								# make new style (style is the list of elements we need here)
				#~ print('creating new font')
				self.create_new_font(style,'sel.first','sel.last')		# style here is the new list to be turned into a font
				
				#~ DPRINT(self.text.tag_names('sel.first'),'ALL TAG NAMES after edit')
				#~ print('end... is the change in place?')

		def change_style_non_select(self,requested_change): #what to do when no text is selected
			cursor = self.text.index('insert')
			#~ print('change style not selected')
			w, w_start, w_end, w_len = self.word_at_index(cursor +'-1c')
			if cursor in (w_start, w_end):				#cursor is at start or end, turn overide state on with style	
				#~ print('cursor at start or end')
				if cursor == w_end:
					cursor = cursor+'-1c'				#results are gotten from after the index
				current_tags = self.text.tag_names(cursor)
				current_tag = current_tags[-1]
				if requested_change not in self.styles[current_tag]:	#ADD request to next char
					REMOVE = False
				else:													#REMOVE request from next char
					REMOVE = True
				style = self.check_styles(requested_change,current_tag,remove=REMOVE)
				
				if type(style) is not str:						#style is the key of the style (already created)
					#~ print('creating new font')
					style = self.create_new_font(style)	
						
				self.overide_state   = style
				print()
				print('SET OVERIDE STYLE',style)
				print('-----------Checking Button States----')
				#~ print('Cursor position :',cursor,'text',self.text.get(cursor))
				#~ print('All tags at cursor',self.text.tag_names(cursor))
				with ignored(IndexError):
					current_tag = self.text.tag_names(cursor)[-1]
					print('cursor is here',self.text.index(cursor))
					print('All attributes in last tag',self.styles[current_tag])
				# Toggleing the requested change
				if type(requested_change) == tuple: 	#so far size and font family are passed in as tuples
					ref = requested_change[0]	
				else:
					ref = requested_change
				with ignored(KeyError,AttributeError):
					if REMOVE == True:	#as we are removing a style, relseas the button	
						self.button_state_change(self.button_references[ref], 0)
					else:
						self.button_state_change(self.button_references[ref], 1)
			else:								#cursor is in middle
				print('CURSOR IN MIDDLE')
				tag_at_inital_cur_pos = self.text.tag_names(cursor)[-1]
				current_tags = self.text.tag_names(cursor)
				print(current_tags)
				if requested_change not in self.styles[tag_at_inital_cur_pos]:	#ADD request to word
					REMOVE = False
					#~ self.text.tag_remove(current_tags[0],w_start, w_end)	#removing default tag
				else:															#REMOVE request from wor
					REMOVE = True
					self.text.tag_add('default',w_start, w_end)				#adding default tag
				hold_styles = [] 									#style required for each char will be saved in here
				index = w_start	
				for num in range(0,w_len):							#does a style exist fuflling requirements for each char?
					print('Looping time:',num)
					current_tags = self.text.tag_names(index)		#tags  at characher   
					current_tag = current_tags[-1]

					style = self.check_styles(requested_change,current_tag,remove=REMOVE)
					
					if style != current_tag:					# no need to add it again!
						print('NOT EQUAL')
						if type(style) is str:						#style is the key of the style (already created)
							print(style,'using this already created style')
							self.text.tag_add(style, index)
							self.text.tag_remove(current_tag, index)
			
						else:												
							print('creating new font')
							self.create_new_font(style,index)		# style here is the new list to be turned into a font
					index = index+'+1c'
			
		def check_styles(self,requested_change,current,remove=False):
			#check if an xml tag is already present for the required + new settings
			#returns either the key or the list of settings for a new style to be created
			if remove:			
				required_style = [item for item in self.styles[current] 		#remove the change from current values
										if item != requested_change]
			else:		#add change
				if current == 'sel':	#sel has to be handled specifically, i.e not saving a list with it in the styles dictionary
					#~ print('CURRENT TAG = SEL')
					required_style = [requested_change]
					#~ print('hi hi hi',type(requested_change))
				else:
					print(self.styles[current][:],'CURRENT STYLE')
					required_style = self.styles[current][:]	#copy the list	
					required_style.append(requested_change)		#add the change from current values		
			#~ print('The required style is: ',required_style)
		
			for key,items in self.styles.items(): 	            # find out if our style exists already
				print (key,'=> ',items)
				if set(items) == set (required_style):	# unordered equality check (not taking duplicates into account)
					print(items,required_style ,'match')
					return key			# style already exists
			else:		#if no matches
				#~ print('No match found !')
				if type(required_style) == list: #this check was put in because of the first 'sel'
					return required_style
				else: 
					return [required_style]

		def create_new_font(self,style,first_index=False,last_index = False):
			#Creates a new font setting for the passed in style
			#Adds it to our styles dict and applies it to the index
			new_font = tkinter.font.Font(self.text, self.text.cget("font"))	#Get base font options
			new_name = self.make_name(style) 
			#~ print(new_name,'new name of the new font')
			for item in style:								# configure font attributes 
				try:
					print(self.option_list[item], 'configured item')
					new_font.configure(**self.option_list[item])	#option_list  contains the option name for the setting
				except KeyError:			#cannot serialize the int with Element tree so had to make it str
					print(item, 'configured item')
					print('OK ITEM PRINTING FOR TES',item)
					if item[0] == 'size':			#http://effbot.org/tkinterbook/tkinter-widget-styling.htm
						new_font.configure(size = item[1])
					if item[0] == 'family':
						new_font.configure(family = item[1])
					if item[0] == 'background':
						new_font.configure(background = item[1])
					if item[0] == 'foreground':
						new_font.configure(foreground = item[1])
			self.text.tag_configure(new_name, font=new_font)	#add tag to font
			try:			# throws except when i want to only update to one charachter
				self.text.tag_add(new_name, first_index, last_index)#tag is added to the widget at selected text positions
			except tk.TclError:
				try:
					self.text.tag_add(new_name, first_index)
				except tk.TclError:			#no index values passed so don not add tag
					pass
			self.styles[new_name] = style										
			return new_name		#this is only used in like 1 out of 3 calls to this function fyi
		def make_name(self,style):	#
			#~ makes a new name for the tk and xml tag,
			#~ If an entire line is selected, make a p tag,
			#~ other wise make a span tag  			

			if 'full line selected':	#p tag
				tag = 'p' 
			else: 						#span tag TBD
				tag = 'T'
			last = 1
			versions = [int(item[-1]) for item in self.styles.keys() if item[0] == tag]	#group numbers at end according to tag
			for num in versions:	#generate a unique number
				if last not in versions:	#num is  uniquie (will return numbers if the list has skips so p1 p2 p5,
					#~ print('checking if last not in
					break
				else:				#number already exists
					last += 1
			return tag+str(last)	#looped till end, then it was plussed so just return new value

def line_count(text):	#http://stackoverflow.com/questions/4609382/getting-the-total-of-lines-in-a-tkinter-text-widget
	return int(text.index('end-1c').split('.')[0])
			
if __name__ == '__main__': 
	pass
