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
import functools
import logging
import sys
import time
import os
import xml.dom.minidom # for testing only http://stackoverflow.com/questions/749796/pretty-printing-xml-in-python
from contextlib import suppress
from pprint import pprint

from timstools import InMemoryWriter, unique_int
from tkquick.gui.tools import toggle, tkinter_breaker

#~ print(help(ET.Element.getiterator))
#~ root = self.xml_tree.getroot()               #unavalibel when pasrse from str, .. bug in element tree?
class MixInText:
        """
        General Mix in methods for tkinter Text widget
        """
        @staticmethod
        def named_partial(name, func, *args):                           # TBD see here.. http://stackoverflow.com/questions/11040098/cannot-pass-arguments-from-the-tkinter-widget-after-function#_=_
                # After method throws an attribute error because there is no
                # __name__ method found when using functools.partial,this resolves that
                # returns the function
                function = functools.partial(func, *args)
                function.__name__ = name
                return function

        def word_at_index(self, cursor):                        # TBD IS THERE A BUIIN FOR THIS? CHECK
                '''Returns start and indexs of a word at given cursor position'''
                text = self.text
                if text.get(cursor) in (' ','\n'):              # right extremity of the word
                        end = cursor
                elif cursor == text.index('end-1c'):    # if at end of text widget, end is alwas with new line so move one back
                        end = cursor
                else:
                        holder = cursor+'+1c'
                        for i in range(0,9999999999999999):
                                if text.get(holder) in (' ','\n'):
                                        end = holder
                                        break
                                elif str(holder).split('+')[0] == text.index('end-1c'): #the str looks like 1.0+1c+1c etc
                                        end = holder
                                        break
                                else:
                                        holder = holder +'+1c'
                holder = cursor
                if text.get(holder+'-1c') == '\n':      #left extremity of the word
                        start = cursor
                        #~ print('FOUD START GIVEN',start)
                elif text.index(cursor) == '1.0':       #if at pos 1.0
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

        def tag_indexes(self, tag):
                '''yields the start and end indexs for a tag'''
                # the second pareametr of slice is a step 
                # http://stackoverflow.com/questions/4647050/collect-every-pair-of-elements-from-a-list-into-tuples-in-python
                
                #~ yield self.text.tag_ranges(tag)[0::2], self.text.tag_ranges(tag)[1::2]
                tag_sections = zip(self.text.tag_ranges(tag)[0::2], self.text.tag_ranges(tag)[1::2]) 
                for start, end in tag_sections:
                        yield start, end
                        #~ print('tag: %s, start and end : %s,  %s, text: %s'% (tag,start,end,self.text.get(start,end)))
                        #~ yield start, self.text.get(start,end)
        @staticmethod
        def button_state_toggle(but):
                if toggle(but):
                        #~ print(1)
                        but.config(default='active')
                else:
                        #~ print(2)
                        but.config(default='normal')
        @staticmethod
        def parse_but_ref(attribute):
                '''
                Parses the requested change into the corresponding button reference key
                '''
                if type(attribute) == tuple:                    # So far size and font family are passed in as tuples
                        attribute = attribute[0]
                elif attribute == 'solid':
                        attribute ='underline'                          # Hacky..
                return attribute

        @staticmethod
        def button_state_change(but, state, style_settings):                    # in cases wher i want to change values but based on a variable not simple toggle
                '''
                Used for setting TTK buttons as selected or unselected.

                str 'toggle' to toggle from the current state
                1 to set default to active              - Pressed state
                0 to set default state to normal

                To see how to create the style of the selected state see below.
                Or see button_styling.py used by demo.py, get from github

                tkinter.ttk.Style().theme_create("toggle", "default", settings={
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
                        )}
                })

                style.theme_use('toggle')
                '''
                #~ print('button state toggle called')
                # When the function is called by the user simply moving the cursor in the wiget
                # We a given all the settings and we loop over only the tuples
                # When the user has changed the style, we are given the value directly, but the call
                # is put into a tuple so it matches the filtereing below, e.g (requested_change,)       #tbd remove this?
                                # Ttk button handling
                if state == 'toggle':
                        #~ print('TOGGLEING Value of cget : ',but.cget('default'))
                        if str(but.cget('default')) == 'normal': #button state not pressed
                                #~ print('set to active')
                                but.config(default='active')
                        else:
                                but.config(default='normal')
                elif state:
                        #~ print('Active')
                        but.config(default='active')
                else:
                        #~ print('Normal')
                        but.config(default='normal')
        @staticmethod
        def menu_state_change(tk_var, attrib, style_settings):                          # Tbd how to make the colour changer work with this? str var set up to a style setting?
                for item in filter(lambda x: type(x) == tuple, style_settings):
                        if attrib == item[0]:
                                tk_var.set(item[1])
        @tkinter_breaker
        def paste_text(self):
                #~ data = self.text.selection_get(selection='CLIPBOARD')        # only works for text copied after program opened
                # Delete selected text
                with suppress(tk.TclError):
                        clipboard = self.text.clipboard_get()
                        start = self.text.index('sel.first')
                        end = self.text.index('sel.last')
                        self.text.delete(start, end)
                start = self.text.index('insert')
                self.text.insert('insert', clipboard)
                end = self.text.index('insert')
                index = start
                def tag(index, end):
                        #~ print('tagging')
                        while index != end:
                                #~ print(index)
                                self.text.tag_add('default', index)
                                index = self.text.index(index+'+1c')
                self.text.after(1,tag,index,end)

        @tkinter_breaker
        def copy_text(self):
                self.text.clipboard_clear()
                selected = self.text.get('sel.first', 'sel.last')
                self.text.clipboard_append(selected)

        def let_update_tag(self, current_tags, current_tag, index):
                        self.text.tag_add(current_tag, index)
                        with suppress(IndexError):
                                #Fails on 1.0
                                if current_tags[0] != current_tag:
                                        self.text.tag_remove(current_tags[0], index)

        def default_tag(self, event):
                # Controls adding the style tag on new text insert,
                # after being called will reset the self.overide_state variable
                text = event.widget
                # x01 is ctrl a, i need to find a better way of blocking out unwanted hotkeys my current filterint sucks TBD
                if event.char not in ('', '\x01') and event.keysym not in ('BackSpace','Delete', 'Escape'):
                        cursor = text.index('insert')
                        char_before = text.index(cursor + '-1c')
                        current_tags = text.tag_names(char_before)
                        if self.overide_state:
                                current_tag = self.overide_state
                        else:
                                try:
                                        if current_tags[0] == 'sel':
                                                # Take readings from start of selection as the rest gets deleted on new insert!
                                                cursor = text.index('sel.first')
                                                current_tags = text.tag_names(cursor)
                                        current_tag = current_tags[-1]
                                except IndexError:
                                        current_tag = 'default'
                                row, col = cursor.split('.')
                                if col == '0' and row != '1':
                                        # if at start of row, and text exists to the right of the cursor take that style
                                        def let_text_get():
                                                if text.get(cursor+'+1c') != '\n':
                                                        # data exists after the cursour, so take that setting
                                                        current_tags = text.tag_names(cursor+'+1c')
                                                else:
                                                        # get style from last line, which is default behavior
                                                        current_tags = text.tag_names(cursor+'-1c')
                                                current_tag = current_tags[-1]
                                                text.tag_add(current_tag, cursor)
                                                if current_tags[0] != current_tag:
                                                        # remove old tag
                                                        text.tag_remove(current_tags[0], cursor)
                                        text.after(1, let_text_get)
                                        return
                        text.after(1, self.named_partial('letupdate', self.let_update_tag, current_tags, current_tag, cursor))
                        text.after(1, self.named_partial('randomname', self.check_button_state, event))
                        if event.char != ' ':
                                # Do no reset on space
                                self.overide_state = 0
                elif event.keysym in ('Left','Down','Right','Up','BackSpace'):
                        # Button indent checking on arrow key pressed #tbd this should probably be put somewhere else has nothing to do with default tag
                        text.after(1, self.named_partial('arrowbutstate',self.check_button_state, event))
                        
        def check_button_state(self, event=None):
                # On mouse over and arrow keys or backspace this gets called
                '''Indents / Unindents our buttons and sets menus to correct values,
                call this after moving the cursor position using insert to update
                the bold/italic/underline buttons'''
                cursor = self.text.index('insert')
                try:
                        current_tag = self.text.tag_names(cursor)[-1]
                        style_settings = self.styles[current_tag]
                except IndexError:
                        style_settings = ''
                except KeyError:
                        # sel tag being passed in
                        return
                
                with suppress(KeyError,AttributeError):
                        for attrib, button in self.button_references.items():
                                # Turning all button states off, This has to be done by analyzing the current position
                                if attrib not in ('family','size','colour'):
                                        self.button_state_change(self.button_references[attrib], 0, style_settings)
                with suppress(IndexError):
                        logging.info('Current tags and style {0} {1}'.format(self.text.tag_names(cursor), self.styles[self.text.tag_names(cursor)[-1]]))
                if not cursor.split('.')[-1] == '0':
                        # Not at start of a row
                        prev_cursor = cursor+'-1c'
                else:
                        # Irregular behavior at start of row
                        prev_cursor = cursor

                try:
                        current_tag = self.text.tag_names(prev_cursor)[-1]
                        style_settings = self.styles[current_tag]
                except IndexError:
                        # when the text widget is empty
                        return
                for attrib in self.styles[current_tag]:
                        # Turning on Buttons, This is done by analying the previous char
                        attrib = self.parse_but_ref(attrib)
                        with suppress(KeyError,AttributeError):
                                if attrib not in ('family','size', 'foreground','background'):
                                        self.button_state_change(self.button_references[attrib], 1, style_settings)
                                else:
                                        self.menu_state_change(self.button_references[attrib], attrib, style_settings)
                self.overide_state = 0                          # back to default behavior

        def font_from_style(self, new_font, name, style):
                # configure font attributes
                for item in style:
                        try:
                                new_font.configure(**self.option_list[item])
                        except KeyError:
                                if item[0] == 'size':
                                        if os.name == 'posix':
                                                new_font.configure(size=int(item[1])-2)
                                        else:
                                                new_font.configure(size=item[1])
                                if item[0] == 'family':
                                        new_font.configure(family=item[1])
                                if item[0] == 'background':
                                        self.text.tag_configure(name, background=item[1])
                                if item[0] == 'foreground':
                                        self.text.tag_configure(name, foreground=item[1])
                        self.text.tag_configure(name, font=new_font)

        @staticmethod
        def remove_default_bindings(text):
                '''
                Couldn't get the unbind command to work so this is how i silence
                those pesky tkinter binds!
                
                If you plan to use the key, you need to ensure to return "break"
                use ma tkinter_breaker function, just a try finally
                
                this could also be an option
                http://stackoverflow.com/questions/6433369/deleting-and-changing-a-tkinter-event-binding-in-python
                '''
                # Remove Default Bindings and what happens on insert etc
                def null(event):
                        print('removed binding')
                        return "break"
                text.bind('<Control-Key-d>', null)      # Delete
                text.bind('<Control-Key-t>', null)      # Switch chars
                text.bind('<Control-Key-h>', null)      # Backspace
                text.bind('<Control-Key-k>', null)      # Delete Rest of line
                text.bind('<Control-Key-o>', null)      # Shift line down
                text.bind('<Control-Key-o>', null)      # Shift line down
                text.bind('<Control-Key-r>', null)      # Home
                text.bind('<Control-Key-i>', null)      # Tab
                text.bind('<Control-Key-p>', null)      # Paste
                # text.bind('<Control-Key-p>', lambda e:print(1))
                #~ text.unbind('<Control-Key-i>')       # THIS UNBIND METHOD DOESN"T WORK FML
        
        def select_all(self, event):
                text = event.widget
                cursor_row = int(text.index('insert').split('.')[0])
                end_row = int(text.index('end').split('.')[0])
                cursor = text.index('insert')
                if end_row == cursor_row + 1 and text.get(cursor) != '\n':
                        end = 'end' + '-1c'
                else:
                        end = 'end'
                text.tag_add('sel', '1.0', end)

        
class TagManager(MixInText):
                """
                For Demo Code do
                >>> from tttt import demo
                >>> demo.start()

                The behaviour of adding tags was modelled from libre office

                to change the default style of the widget,
                simple use the config method on text widget.
                Bold, Italic and Underline are not supported for a default style.
                
                Make sure to initialize your font family and size selection
                widgets to your default

                ----- Short Example -----
                tag_manager = TagManager(TextWidget):

                # Load data from database etc
                tag_manager.load_xml(data)

                # Save your data
                data = tag_manager.save()

                # Add or Remove a Style
                tag_manager.change_style(required change here)
                
                Some more config options
                
                """
                option_list = {'bold':{'weight':'bold'},
                                                'solid':{'underline':1},
                                                'italic':{'slant':'italic'},
                                                'overstrike':{'overstrike':1}}

                def __init__(self, text):
                        self.overide_state = 0                                                                  # If the state is active it will overide the default behabvior of style grabbing
                        self.text = text
                        self.text.bind('<Key>',lambda e: self.default_tag(e))
                        self.text.bind('<Button-1>',lambda e: self.text.after(1, self.named_partial('butclick', self.check_button_state,e)))
                        self.text.bind('<Control-Key-v>',lambda event:self.paste_text())
                        self.text.bind('<Control-Key-V>',lambda event:self.paste_text())
                        self.text.bind('<Control-Key-c>',lambda event:self.copy_text())
                        self.text.bind('<Control-Key-C>',lambda event:self.copy_text())
                        @tkinter_breaker
                        def test(event):                        
                                tags = self.text.tag_names(self.text.index('insert'))
                                pprint(tags)
                                print(self.styles[tags[0]])
                                sdfjaldkf               #TBD FIND OUT WHY THIS ISN"T RAISING AN ERROR LOL
                        self.text.bind('<Control-Key-t>', test)
                
                        # Setting up default settings for the widget
                        font = self.text.cget('font')[0:].split('}')
                        if font[0][0] == '{':                                                                   # Font families that have spaces are in brackets
                                font[0] = font[0][1:]
                        try:
                                size = font[1].split(' ')[1]
                        except IndexError:
                                size = 12
                        default_tag = [('family',font[0]),
                                                        ('size',size),
                                                        ('foreground', self.text.cget('foreground'))]
                        self.styles = {'default':default_tag}
                        self.text.config(font=(font[0], size))                                  # Cannot have any sort of bold,italic,solid for default setting
                        
                        self.load_style_tags()

                # Make buttons not take focus when clicked
                @property
                def button_references(self):
                        return self._but_ref
                @button_references.setter
                def button_references(self, adict):
                        self._but_ref = adict
                        self._but_refs = adict
                        for button in self._but_refs.values():
                                try:
                                        button.configure(takefocus=0)
                                except AttributeError:
                                        pass

                def load(self, data):
                        '''
                        pass in xml data that has been previously saved
                        to load it as normal text
                        '''
                        #~ if data.strip():                                                                             # Peparing to pretty print for debug
                                #~ xmlt = xml.dom.minidom.parseString(data)
                                #~ pretty_xml_as_string = xmlt.toprettyxml()
                                #~ with open('xml_on_load.txt','w') as f:                       # This file is written for debug purposes
                                        #~ f.write(pretty_xml_as_string)
                        with suppress(ET.ParseError):                                                   # if parse error i.e no xml tags
                                tree = ET.fromstring(data)
                                auto_styles = tree.find('automatic-styles')
                                body = tree.find('body')
                                # Recreating style options
                                for style in auto_styles:
                                        key = style.get('name')
                                        values = []
                                        text_properties = style.find('text-properties')
                                        weight                  = text_properties.get('weight')
                                        font_style              = text_properties.get('font-style')     # italic
                                        underline_style = text_properties.get('text-underline-style')
                                        font_size               = ('size',text_properties.get('font-size'))
                                        bg                              = ('background',text_properties.get('background-color'))
                                        fg                              = ('foreground',text_properties.get('color'))
                                        font_name               = ('family',text_properties.get('font-name'))
                                        overstrike              = text_properties.get('text-line-through-type')

                                        # overstrike name needs to be remaped TBD, do this better/more scaleable
                                        if overstrike:
                                                overstrike = 'overstrike'

                                        values = [weight,font_style,underline_style,font_size,font_name,bg,fg,overstrike]
                                        filtered = []
                                        # Remove values with None
                                        for item in values:
                                                try:
                                                        if item[1] is not None:
                                                                filtered.append(item)
                                                except TypeError:
                                                        if item is not None:
                                                                filtered.append(item)
                                        self.styles[key] = filtered     
                        
                        self.load_style_tags()

                        # Inserting text into widget
                        with suppress(UnboundLocalError):
                                body_iter = body.getiterator()
                                body_iter.__next__()
                                for xml_tag in body_iter:
                                        # position moves after text is inserted so save it now
                                        original_index = self.text.index('insert')
                                        self.text.insert('insert',xml_tag.text)
                                        ending_index = self.text.index('end -1c')
                                        self.text.tag_add(xml_tag.get('style-name'), original_index, ending_index)
                        self.text.after(20, lambda: self.check_button_state(None))

                def load_style_tags(self):
                        # loading the styles into text tags
                        for name, style in self.styles.items():
                                new_font = tkinter.font.Font(self.text, self.text.cget("font"))
                                self.font_from_style(new_font, name, style)

                def save(self):
                        """
                        Returns all data from the text widget formatted with xml
                        following libre office standards
                        
                        Store as you please

                        data = my_xml_text.save()
                        """
                        data = self.text.get('1.0', 'end'+'-1c')        # tbd a new line gets appended on every new load/save, this seems more like a quickfix
                        self.xml_setup()
                        self.convert_text_to_xml(data)  
                        xml_data = self.save_style_info()
                        #~ xmlt = xml.dom.minidom.parseString(xml_data) #This code block is for debugging purposes
                        #~ pretty_xml_as_string = xmlt.toprettyxml()
                        #~ with open('xml_on_save.txt','w') as f:
                                #~ f.write(pretty_xml_as_string)
                        return xml_data

                def xml_setup(self):
                        # create standard xml template
                        root = ET.Element("document-content")
                        auto_styles = ET.SubElement(root, "automatic-styles")
                        body = ET.SubElement(root, "body")
                        tree = ET.ElementTree(root)
                        self.xml_tree = tree

                def convert_text_to_xml(self,new_data):
                        holder = {}
                        body = self.xml_tree.find('body')
                        for tag in self.styles.keys():
                                for start_index, end_index in self.tag_indexes(tag):
                                        text = self.text.get(start_index, end_index)
                                        # add text to dict with key as start pos
                                        holder[str(start_index)] = [tag, text]
                                        
                        for i, pos in enumerate(sorted(holder.keys(), key=lambda s: [int(x) for x in s.split(".")])):
                                row, col = pos.split('.')
                                row, col = int(row), int(col)
                                tag_name, text = holder[pos]
                                tag_type = tag_name
                                if tag_type[0] == 'T':  # change to a span tag TBD
                                        tag_type = 'span'
                                else:
                                        tag_type = 'p'          # p type tag
                                XML_tag = ET.SubElement(body, tag_type)         #tag
                                XML_tag.set('style-name', tag_name)                     #style name
                                XML_tag.text = text

                def save_style_info(self):      
                        # saves the style info in automatic styles xml tag info
                        auto_styles = self.xml_tree.find('automatic-styles')
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
                                with suppress(IndexError):
                                        for setting in values:
                                                if setting[0] =='size':
                                                        text_properties.set('font-size', str(setting[1]))
                                                elif setting[0] =='family':
                                                        text_properties.set('font-name', setting[1])
                                                elif setting[0] =='background':
                                                        text_properties.set('background-color', setting[1])
                                                elif setting[0] =='foreground':
                                                        text_properties.set('color', setting[1])
                        # in memory file object
                        mw = InMemoryWriter()
                        self.xml_tree.write(mw)
                        return mw.data[0].decode('utf-8')

                @tkinter_breaker
                def change_style(self,requested_change):
                        '''
                        pass in desired style change

                        bold, italic, underline, overstrike

                        send in size as an interger     ('size',value)
                        send in a font name as                  ('family',value)
                        send in colour:                 ('foreground',value)

                        If binding to hotkeys bind like this
                        text.bind('<Control-Key-b>',..

                        insead of like this
                        text.bind('<Control_L><b>',..
                        '''
                        #~ if requested_change == 'underline': requested_change = 'solid' #much better to call underline not solid, mapping for convienecne
                        # button ref requires it to be solid though
                        try:
                                cursor = self.text.index('insert')
                                self.change_style_selected(requested_change)
                                # Restore cursor position
                        except(tk.TclError) as err:
                                if not 'sel' in str(err):
                                        print('unexpected error ')
                                        raise err
                                else:
                                        self.change_style_non_select(requested_change)
                        # Refocuses after clickng on button
                        self.text.focus_force()
                        
                def change_style_selected(self, requested_change):
                        logging.info('Changing style SELECTED')
                        current_tags = self.text.tag_names('sel.first')
                        current_tag = current_tags[-1]
                        if current_tag == 'sel':
                                print('cur tag was equal to sel')
                                sys.exit()
                        if requested_change not in self.styles[current_tag]:
                                logging.info('add request@ %s , %s' % (self.text.index('sel.first'),self.text.index('sel.last')))
                                BUTTON_STATE = True
                                REMOVE = False
                        else:
                                logging.info('remove request @ %s , %s' % (self.text.index('sel.first'),self.text.index('sel.last')))
                                BUTTON_STATE = False
                                REMOVE= True
                        # Button States TBD apply DRY
                        style = self.check_styles(requested_change, current_tag, remove=REMOVE)
                        with suppress(KeyError):
                                attrib = self.parse_but_ref(requested_change)
                                if attrib not in ('family','size', 'foreground','background'):
                                        self.button_state_change(self.button_references[attrib], BUTTON_STATE, (requested_change,))
                                else:
                                        self.menu_state_change(self.button_references[attrib], attrib, style)

                        self.change_style_range(self.text.index("sel.first"),
                                                                        self.text.count('sel.first', 'sel.last', 'chars')[0],
                                                                        requested_change,
                                                                        REMOVE=None)

                def change_style_non_select(self,requested_change):
                        cursor = self.text.index('insert')
                        w, w_start, w_end, w_len = self.word_at_index(cursor)
                        if cursor in (w_start, w_end) or self.text.get(cursor) in(' ', '\n'):
                                logging.info('Changing style - No Selected Text - Cursor @ start or end of word')
                                if self.text.get(cursor) in (' ', '\n') or cursor == w_end:
                                        logging.info('Ok cursor at end of a word')
                                        cursor = cursor+'-1c'
                                else:
                                        logging.info('Ok curosr at start of word')
                                current_tags = self.text.tag_names(cursor)
                                current_tag = current_tags[-1]

                                if not self.overide_state:
                                        if requested_change not in self.styles[current_tag]:
                                                REMOVE = False
                                        else:
                                                REMOVE = True
                                else:
                                        if requested_change in self.styles[self.overide_state]:
                                                REMOVE = True
                                        else:
                                                REMOVE = False
                                if self.overide_state:
                                        current_tag = self.overide_state
                                style = self.check_styles(requested_change, current_tag, remove=REMOVE)
                                if type(style) is not str:
                                        style = self.create_new_font(style)
                                self.overide_state = style
                        else:
                                logging.info('Changin style - No Selected Text - Cursor in "MIDDLE" of word')
                                tag_at_prev_pos = self.text.tag_names(cursor+'-1c')[-1]

                                if requested_change not in self.styles[tag_at_prev_pos]:
                                        REMOVE = False
                                else:
                                        REMOVE = True

                                self.change_style_range(w_start, w_len, requested_change, REMOVE)

                        attribute = self.parse_but_ref(requested_change)
                        with suppress(KeyError, AttributeError, tk.TclError):
                                if REMOVE == True:
                                        logging.info('Unindenting Button')
                                        self.button_state_change(self.button_references[attribute], 0, (requested_change,))
                                else:
                                        logging.info('Indenting Button a style')
                                        self.button_state_change(self.button_references[attribute], 1, (requested_change,))

                def check_styles(self, requested_change, current_tag, remove=False):
                        # Check if a tag is already present for the required + new settings
                        # Returns either the key or the list of settings for a new style to be created
                        # The old key or list will only be returned if that style doesn't exist elsewhere...
                        if remove:
                                logging.info('removing '+ str(requested_change)+' from settings from '+current_tag)
                                if type(requested_change) in (tuple, list):
                                        # a menu list item such as size or font
                                        required_style = self.styles[current_tag]
                                else:
                                        required_style = [item for item in self.styles[current_tag]
                                                                                if item != requested_change]
                        else:
                                logging.info('adding '+ str(requested_change)+' to settings from '+current_tag)
                                if type(requested_change) in (tuple, list):
                                        # a menu list item such as size or font
                                        required_style = []
                                        for item in self.styles[current_tag]:
                                                # remove the old size
                                                if type(item) not in (tuple, list):
                                                        required_style.append(item)
                                                elif requested_change[0] != item[0]:
                                                        required_style.append(item)
                                else:
                                        required_style = self.styles[current_tag][:]
                                required_style.append(requested_change)
                        # find out if our style exists already
                        for key, items in self.styles.items():
                                if set(items) == set(required_style):
                                        return key
                                        break
                        # this check was put in because of the first 'sel'
                        if type(required_style) == list:
                                if required_style:
                                        return required_style
                                else:
                                        logging.info('Assigning default font style')
                                        return 'default'
                        else:
                                print('Required still being put in a list')
                                sys.exit()
                                return [required_style] # tbd still required??

                def create_new_font(self, style, first_index=False, last_index=False):
                        # Creates a new font setting for the passed in style
                        # Adds it to our styles dict and applies it to the index
                        new_font = tkinter.font.Font(self.text, self.text.cget("font"))                         # Get base font options
                        name = self.make_name(style)
                        logging.info('Creating a  new font {0} with settings: {1}'.format(name, style))
                        self.font_from_style(new_font, name, style)
                        try:
                                self.text.tag_add(name, first_index, last_index)
                                logging.info('Successfully applied font to a RANGE of text')
                        except tk.TclError:
                                try:
                                        self.text.tag_add(name, first_index)
                                        logging.info('Applied font to a single character')
                                except tk.TclError:
                                        logging.info('No font settings applied to text! returning style for use with overide style')
                        self.styles[name] = style
                        return name

                def make_name(self,style):
                        #~ If an entire line is selected, make a p tag,
                        #~ other wise make a span tag
                        if 'full line selected':        # p tag
                                tag = 'p'
                        else:                                           # span tag TBD to meet same spec as open office
                                tag = 'T'
                        versions = [int(name[1:]) for name in self.styles.keys() if name[0] == tag]
                        return tag+str(unique_int(versions))

                def change_style_range(self, range_start_index, range_len, requested_change, REMOVE=None):
                        # Each letter in a word keeps all its orignal settings
                        index = range_start_index
                        for i in range(0, range_len):
                                current_tags = self.text.tag_names(index)
                                current_tag = current_tags[-1]
                                if REMOVE == None:
                                        # Calculating style for every char based on its index
                                        if requested_change not in self.styles[current_tag]:    # tbd do you need the current_tag sel bit
                                                style = self.check_styles(requested_change, current_tag, remove=False)
                                        else:
                                                style = self.check_styles(requested_change, current_tag, remove=True)
                                else:
                                        # Calculating style based on original index
                                        style = self.check_styles(requested_change, current_tag, remove=REMOVE)
                                if style != current_tag:
                                        if type(style) is str:
                                                # Using this already created style
                                                self.text.tag_add(style, index)
                                        else:
                                                # Creating and applying new font to this character
                                                self.create_new_font(style, index)
                                        self.text.tag_remove(current_tag, index)
                                index = index+'+1c'

def line_count(text):
        return int(text.index('end-1c').split('.')[0])

if __name__ == '__main__':
        import demo
        import platform

        LOG_FILE = 'log.log'

        def logger_setup(log_file):
                logging.basicConfig(filename=log_file,
                                filemode='w',
                                level=logging.DEBUG,
                                format='%(asctime)s:%(levelname)s: %(message)s')
                logging.debug('System is: %s' % platform.platform())
                logging.debug('Python archetecture is: %s' % platform.architecture()[0])
                logging.debug('Machine archetecture is: %s' % platform.machine())

        logger_setup(LOG_FILE)
        demo.start()

### References
# http://effbot.org/tkinterbook/tkinter-widget-styling.htm
# http://stackoverflow.com/questions/4609382/getting-the-total-of-lines-in-a-tkinter-text-widget
'''
SCRIBBLES

tag cleanup! run this in a thread or something
if not self.text.tag_ranges(current_tag):
        print('doesnt exist elsewehre! safe to use!')

copy and pasting formatting

Holy shit the entire data set is analyzed each time it saves... i guess it works!
'''
