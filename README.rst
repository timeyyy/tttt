
.. image:: http://i101.photobucket.com/albums/m58/timeyyy_da_man/coloring_pencils.jpg
	:alt: coloring pencils!
	:align: right
	:scale: 40 %
	
tttt - tims tkinter text tags
=============================

Save and load tags for the tkinter text widget using open office format xml

Features
--------

* Super easy to use api, All the commands you will need are below!
* Automatically indent buttons on selection
* Bold, Italic, Underline, Overstrike, Fonts, Sizes
* Behavour of adding and removing tags is modeled on libre office

Installation
------------

pip3 install tttt

Usage
-----

There is a `demo picture <https://github.com/timeyyy/tttt/wiki/Demo-Code>`_ avaliable

.. code-block:: python

	from tttt import XmlManager

	tag_manager = XmlManager(text)


bind these to your callback buttons or hotkeys

.. code-block:: python

	tag_manager.change_style('bold') 
	tag_manager.change_style('italic')
	tag_manager.change_style('solid') 			# underline 
	tag_manager.change_style(('family',value)) 
	tag_manager.change_style(('size',value))
	tag_manager.change_style(('foreground', value))
	tag_manager.change_style(('background', value))

Saving and loading
^^^^^^^^^^^^^^^^^^

.. code-block:: python

	xml_data = tag_manager.save_with_xml()
	tag_manager.load_xml(data)


Configuring Buttons For Indenting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

	tag_manager.button_references = {'bold':bold,
					'italic':italic,
					'underline':underline,
					'family':family_font_menu.var,
					'overstrike':overstrike,
					'foreground':foreground,
					'background':background,
					'size':size_menu.var
					} 
