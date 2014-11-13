tttt - tims tkinter text tags
===========

Save and load tags for the tkinter text widget using open office format xml

Developed with Python3

<img src="http://www.freeimageslive.com/galleries/workplace/office2/preview/coloring_pencils.jpg" alt="pencil icon" width="50%", height="50%" align="right" />


##Features##
* Automatically indent buttons on selection
* Bold, Italic, Underline, Overstrike, Fonts, Sizes
* Behavour of adding and removing tags is modeled on libre office

##Installation##
The plugin is not yet released as a pip. (needs to be a little bit more stable)
There is a [Demo](https://github.com/timeyyy/tttt/wiki/Demo-Code) avaliable

##Usage##

```
from tttt import XmlManager

tag_manager = XmlManager(text)
```
***bind these to your callback buttons or hotkeys***
```
tag_manager.change_style('bold') 
tag_manager.change_style('italic')
tag_manager.change_style('solid') #underline 
tag_manager.change_style(('family',value)) 
tag_manager.change_style(('size',value))
```
***Saving and loading***
```
xml_data = tag_manager.save_with_xml()
data = tag_manager.load_xml(xml_data)
```

##Development / Contributing##
* Check the Github Issue Tracker
* Setting up mail list and dev communications

