from collections import OrderedDict
import contextlib
import json

class InMemoryWriter():
	"""
	Used to defer saving and opening files to later controllers
	just write data to here
	"""
	def __init__(self):
		self.data=[]
	def write(self, stuff):
		self.data.append(stuff)
	def writelines(self, passed_data):
		for item in passed_data:
			self.data.append(item)
	def close(self):
		self.strData=json.dumps(self.data)	#turned into str
class InMemoryReader():	#http://www.diveintopython3.net/iterators.html

	def __init__(self,data):
		self.data=data
	def __iter__(self):
		self.i=0
		return self
	def __next__(self):
		if self.i+1 > len(self.data):	
			 raise StopIteration  
		requested=self.data[self.i]
		self.i+=1
		return requested
			
	def close(self):
		print('in reader close method')
		#~ self.strData=json.dumps(self.data)	#turned into str

@contextlib.contextmanager
def ignored(*exceptions,details=None):
	try:
		yield
	except exceptions as e:
		
		if details and details in str(e):	#skip what was wanting to be skipped
			pass
		elif details:		#if details not in str but details passed in raise
			raise e

def SCREAM(message,note=None,header='$(#)@$() ---SCREAMMM ----!!!!!'):
	"""
	NICE VISABLE MESSAGE FOR DEBUGGING SCREAMMM RAWR
	DO YOU SEE ME KNOW!!!
	"""
	print()
	print('!@#$%^&*()!@#$%^&*(!@#$%^&*-----')
	print()
	if note != None:
		#~ message =[message,'---->',note]
		header =[header,'-->  ', note]
	print(header)
	print(message)
	print()
	print('!@#$%^&*()!@#$%^&*(!@#$%^&*-----')
	print('ENDING THE SCREAM-- IT ALL goes silent now..')
	print()

def DPRINT(message,note=None,header='--------- Debug Below----------'):
	#~ return					# USED FOR NOT PRINTING XD
	"""
	Debug Print, easier to see XD
	"""
	#~ for i in flattenUntil(message,list):
		#~ print('LIST')
		#~ print(i)
	print()
	if note != None:
		#~ message =[message,'---->',note]
		header =[header,'-->  ', note]
	print(header)
	print(message)
	print()

@staticmethod
def PDICT(objD,comparison=None):	#object Dictionary, Prints each key value on a line
	print('----------Start of Dict-----------')
	if type(objD)!=dict:objD=objD.__dict__
	if comparison==None:
		if type(objD)==dict:	
			sortedObj = OrderedDict(sorted(objD.items()))
			for key, value in sortedObj.items():
				print([key,'  ---> 	',value])
	elif type(objD)==dict:	#comparison dict method		### TBD
		sortedObj = OrderedDict(sorted(objD.items()))
		sortedObj2 = OrderedDict(sorted(comparison.items()))
		
		for key,key2 in zip(sortedObj.keys(),sortedObj2.keys()):
			#~ print(key,key2)
			if not sortedObj.get(key2):
				print('First Object: Doesnt contain key :  '+key2+'        from Second Object')
			#~ if not sortedObj2.get(key):
				#~ print(str(comparison)+': Doesnt contain key:'+key+'from :'+str(objD))
	print('----------end of dict----------')

def PTYPE(obj):	#TBD
	print('----------- Printing Types---------')
	for i in obj:
		print(type(obj))
		try:
			print(obj.__name__)#FAILS..
		except:
			pass
	print('-----------Fin Print Types -----------')

def PMETHODS(obj): #prints all methods
	print('-------Printing Methods---------------')
	a=[method for method in dir(obj) if callable(getattr(obj, method))]
	#~ print(a)
	for i in a:
		print(i)
	print('-------------methods fin--------------')
def only_numerics(seq):
    seq_type= type(seq)
    return seq_type().join(filter(seq_type.isdigit, seq))
  
def toggle(btn,tog=[0]):
	'''
	a list default argument has a fixed address
	'''
	tog[0] = not tog[0]
	if not tog[0]:
		#~ btn.config(text='False')
		return False
	else:
		#~ btn.co	nfig(text='True')
		return True
 
def eventClock(timevar,timemax,event,entries=None,maxentries=None):	# returns true when time between events is greater then time specified
	if len(timevar)==2:del timevar[0],timevar[0]
	if len(timevar)==0: 					# if no entry
		timevar.append(event.time)
		print('IF NO ENTRY')
		return False		
	elif len(timevar)==1: 					#if one entry already
		timevar.append(event.time)
		print('IF ONE ALREADY ENTRY')
		if timevar[1]-timevar[0] >=timemax: # time to exit
			print(['IF TIME minus TIME' ,timevar[1]-timevar[0]])
			return True
		elif len(entries) > maxentries:		# Also time to exit
			print(['IF ENTRIES NOT NONE',len(entries),maxentries])
			return True
	print('false +>  ; %s ----- %s' % (timevar,len(timevar)))
	return False
	
def ttk_manual(style, widgets):
	@TraceCalls()
	def iseven(n):
		yield True if n == 0 else isodd(n - 1)
	@TraceCalls()
	def isodd(n):
		yield False if n == 0 else iseven(n - 1)
	print(list(iseven(7)))
	s = style
	if type(widgets) not in (list,tuple):
		widgets = [widgets]

	#~ return
	
	for item in widgets:	# widgets is the passed in items e.g TButton, TLabel etc
		#~ print(list(flatten(s.layout(item))))	
		print(flatten(s.layout(item)))
		#~ holder = []
		#~ for i in flatten(s.layout(item)):
			#~ holder.append(i)
		#~ print()
		#~ print(holder)
		return
	
		print('Layout of Elements: %s -s.layout()'%(item))
		print()
		layout = s.layout(item)
		print(layout[0])
		print()
		print(layout[0][0])
		print()
		print(layout[0][0])
		print()
		print(layout[0][1].keys())
		print()
		#~ print(layout[0][1].keys())
		print()
		for key,value in layout[0][1].items():
			print(key)
			print(	value)
		#~ print(layout[1][0])
		print()
		#~ print(layout[0][01])
			#~ print('printint')
			#~ print(layout)
			#~ print()
		#~ print(s.layout(item))
		
def error_to_bool(func,*args):
	#~ print(args)
	try:
		func(*args)
		#~ print('t')
		return True
	except:
		#~ print('false')
		return False

basestring = (str,bytes)
#~ typestruct = (type(list),type(dict),type(tuple))
import sys
from functools import wraps
class TraceCalls(object):
    """ Use as a decorator on functions that should be traced. Several
        functions can be decorated - they will all be indented according
        to their call depth.
    """
    def __init__(self, stream=sys.stdout, indent_step=2, show_ret=False):
        self.stream = stream
        self.indent_step = indent_step
        self.show_ret = show_ret

        # This is a class attribute since we want to share the indentation
        # level between different traced functions, in case they call
        # each other.
        TraceCalls.cur_indent = 0

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            indent = ' ' * TraceCalls.cur_indent
            argstr = ', '.join(
                [repr(a) for a in args] +
                ["%s=%s" % (a, repr(b)) for a, b in kwargs.items()])
            self.stream.write('%s%s(%s)\n' % (indent, fn.__name__, argstr))

            TraceCalls.cur_indent += self.indent_step
            ret = fn(*args, **kwargs)
            TraceCalls.cur_indent -= self.indent_step

            if self.show_ret:
                self.stream.write('%s--> %s\n' % (indent, ret))
            return ret
        return wrapper
@TraceCalls()
def flatten(l, typestruct=(list,tuple),global_count=''):
	def track(global_count,count):
		return
		global_count = global_count.split(',')
		try:
			current = int(global_count[-1])
		except ValueError:	#errors out on first level
			current = int(global_count[0])
		new = current + count
		global_count.append(str(new))
		global_count = ','.join(global_count)
		string = 'Global: '+global_count+' current: '+str(current)+' new: '+str(new)
		return string
		print(string)
	if global_count:
		#each level is seperated by a comma with deeper levels being on the right
		global_count = global_count + '.0'
		current = 0
	else:
		global_count = '0,'
	
	for i, el in enumerate(l):
		if isinstance(el, typestruct) and not isinstance(el, basestring):
			for j, sub in enumerate(flatten(el)):
				#~ print('USING RECURSION ELEMENT')
				print('Element:',sub,'	:',track(global_count,j))
				return sub
		
		elif isinstance(el,dict) and not isinstance(el, basestring):
			for j, (key, value) in enumerate(el.items()):
				print('dict key:',key,'	:',track(global_count,j))
				return key
				if isinstance(value, typestruct) and not isinstance(value, basestring):
					for k, sub in enumerate(flatten(value)):
						#~ print('USING RECURSION ELEMENT')
						print('dict value:',sub,'	:',track(global_count,k))
						return sub
				else:
					print('dict value:',value,'	:',track(global_count,j))
					return value
			
		else:
			print('top level el I:',el,'	:',track(global_count,i))
			return el

			
def flattenUntil(l,typestruct=(list,dict,tuple)):
	if isinstance(l, typestruct): #only return elements of typestruct dont go deepeter
		for el in l:
			if isinstance(el, typestruct):	#if the next element is a typestruct
				for subel in flattenUntil(el):
					if isinstance(subel,typestruct):
						yield subel
				yield el	
					

def traverse(item):
    try:
        for i in iter(item):
            for j in traverse(i):
                yield j
    except TypeError:
        yield item
        #~ 
def chain(*iterables):
    # chain('ABC', 'DEF') --> A B C D E F
    for it in iterables:
        for element in it:
            yield element		

def sysArgsDict(argv):
	opts = {}
	while argv:
		if argv[0][0] == '-':
			opts[argv[0]] = argv[1]
			argv = argv[2:]
		else:
			opts[argv[0]] = argv[0]
			argv = argv[1:]
	return opts

def inIf(items,Check):
	for i in items:
		if i in check:
			yield i
		else:
			yield False

if __name__ == '__main__':            
	import tttimer
	import time
	import os
	from dbTools import *
	def getWorkbooksOnSystem():
		pathmm=os.getcwd()	# this can change on user settings
		filesInDir=os.listdir(pathmm)
		categories=(os.path.join(os.getcwd(),'categories.txt'))
		categories=open(categories,'r')
		#~ mylist=[]												#this is the comprehension below
		#~ for files in filesInDir:
			#~ for categor in categories:
				#~ x=(os.path.join(pathmm,categor.strip()))
				#~ if os.path.exists(x) == True:
					#~ mylist.append(categor)	
		mylist=[categor.strip() for files in filesInDir for categor in categories if os.path.exists(os.path.join(pathmm,categor.strip())) == True] 
		if len(mylist)>1:	# mylistp-1] doesnt work if only one item so 
			if mylist[-1] =='\n' or mylist[-1] == '/n':	#remove if theres a blank line on the end
				del mylist[-1]
		return mylist
		
	def getWorkbooksOnSystem2():
		pathmm=os.getcwd()	# this can change on user settings
		filesInDir=os.listdir(pathmm)
		categories=(os.path.join(os.getcwd(),'categories.txt'))
		categories=open(categories,'r')
		mylist=[]									#this is the comprehension below
		for files in filesInDir:
			for categor in categories:
				x=(os.path.join(pathmm,categor.strip()))
				if os.path.exists(x) == True:
					mylist.append(categor)	
		#~ mylist=[categor.strip() for files in filesInDir for categor in categories if os.path.exists(os.path.join(pathmm,categor.strip())) == True] 
		if len(mylist)>1:	# mylistp-1] doesnt work if only one item so 
			if mylist[-1] =='\n' or mylist[-1] == '/n':	#remove if theres a blank line on the end
				del mylist[-1]
		return mylist		
		
	def getWorkbooksOnSystem4():
		pathmm=os.getcwd()	# this can change on user settings
		filesInDir=os.listdir(pathmm)
		mylist=[]
		dbshelve = shelve.open('categories') 
		for files in filesInDir:
			#~ print(files)
			for name in dbshelve.keys():
				if files == dbshelve[name]:
					mylist.append(files)
					#~ print('added')
		dbshelve.close()
		return mylist
		
	def getWorkbooksOnSystem3():
		pathmm=os.getcwd()	# this can change on user settings
		filesInDir=os.listdir(pathmm)
		mylist=[]
		dbshelve = shelve.open('categories') 
		mylist=[files for files in filesInDir for name in dbshelve.keys() if files == dbshelve[name]] 

		#~ for files in filesInDir:
			#~ for name in dbshelve.keys():
				#~ if files == dbshelve[name]:
					#~ mylist.append(files)
					#~ print('added')
		dbshelve.close()
		return mylist		
		
		

	d=getWorkbooksOnSystem4()

	timesto=300
	reps=1
	# SHELVE METHOD SLOWER then reading from text file
	#~ a=tttimer.bestoftotal(timesto,reps, getWorkbooksOnSystem)
	#~ print([a, 'using the Comprehension'])
	#~ #time.sleep(10)
	#~ b=tttimer.bestoftotal(timesto,reps, getWorkbooksOnSystem2)
	#~ print([b,' using the Normal method'])
	#~ c=tttimer.bestoftotal(timesto,reps, getWorkbooksOnSystem3)
	#~ print([c,' using the SHELVE COMPREHENSION'])
	#~ d=tttimer.bestoftotal(timesto,reps, getWorkbooksOnSystem4)
	#~ print([d,' using the SHELVE normal'])
	from tkinter import *
	v=VERTICAL
	h=HORIZONTAL
	l=LEFT
	r=RIGHT
	t=TOP
	b=BOTTOM	
	panesList=[(l,v,[(l,v,[(r,v,None)])])]
	#~ basestring = (list,type)
	#~ typestruct = (type(str))
	
	
	#~ root=Tk()									FAILS
	#~ a=Label(root, text='hdddddddddddddddi')
	#~ a.pack()
	#~ import dbTools
	#~ print(dbTools.storeIt(a,'tester','another'))
	#~ root.mainloop()

