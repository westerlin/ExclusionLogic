import re,copy,json,sys,traceback

class DeepFalse():

	def __init__(self,label="<root>"):
		self.label = label

	def __str__(self):
		return str(False)

	def __bool__(self):
		return False

	def __call__(self,arg1=False,arg2=False,arg3=False,arg4=False):
		#import traceback,sys
		#sys.tracebacklimit = 20
		#traceback.format_exc(False)
		raise ExclusionLogicError("You are calling a function from a DeepFalse branch\n\tObject '%s' is not instantiated." %self.label)
		#raise DeepFalseFunctionCallError
		#return False

	def __contains__(self,key):
		return False

	def __repr__(self):
		return repr(False)

	def __iter__(self):
		return self

	def __getattr__(self, name):
		return DeepFalse(self.label+"."+name)

	def __next__(self):
		raise StopIteration

	def __eq__(self, other):
		"""Determines if passed object is equivalent to current object."""
		if other==False: return True
		return False
		#return self.__dict__ == other.__dict__

class ExclusionLogic(object):

	def __init__(self,parent=None,init=None,ID="<root>"):
		self.__current__ = 0
		self.__parent__ = parent
		self.__ID__ = ID
		if init:
			self.set(init)

	def combinations(self,expression):
		pattern =  r'(\{[A-Za-z\_]+\})+'
		predicates = re.split(pattern,expression)
		#print("VARIABLES:",len(predicates),predicates)
		tmp = []
		if len(predicates) >0:
			#print("self."+predicates[0]+"span()")
			try:
				childs = eval("self."+predicates[0]+"span()")
			except Exception as e:
				raise ExclusionLogicError("error evaluating:\n"+"\tself."+predicates[0]+"span()"+"\n\texpression = "+expression)
			for child in childs:
				#scenario = {predicates[1][1:-1]:child}
				#tmp.append(scenario)
				combination = expression.replace(predicates[1],child)
				#print("\t",combination)
				if len(predicates) > 3: 
					combis = self.combinations(combination)
					for combi in combis:
						combi[predicates[1][1:-1]]=eval("self."+predicates[0]+child)
					tmp += combis
				else:
					if len(predicates)>2:
						if eval("self."+combination):
							tmp.append({predicates[1][1:-1]:eval("self."+predicates[0]+child)})		
							#tmp.append({predicates[1][1:-1]:child})		
					else:
						tmp.append({predicates[1][1:-1]:eval("self."+predicates[0]+child)})		
		return tmp		
		#return {predicates[1][1:-1]:combinations}

	def index(self,obj):
		idx = -3
		for k,v in self.__dict__.items():
			#print(k,obj.label())
			if k == obj.label(): return idx
			idx+=1
		return idx	

	def __eq__(self, other):
		"""Determines if passed object is equivalent to current object."""
		if isinstance(other,str):
			return self.label() == other
		if isinstance(other, ExclusionLogic):
			criteria1 = self.__attributes__() == other.__attributes__()
			criteria2 = self.label() in other.span()
			criteria3 = other.label() in self.span()
			return criteria1 or criteria2 or criteria3
		if isinstance(other,bool):
			return other
		if isinstance(other,DeepFalse):
			return False
		raise ExclusionLogicError("Error comparing ExclusionLogic class %s with other object of type %s" %(self.label(),type(other)))
		#return self.__dict__ == other.__dict__

	def toJSON(self):
		qlist = self.__attributes__()
		children ={}
		for q in qlist:
			#print(q)
			try:
				if isinstance(eval("self."+q),ExclusionLogic):
					children[q] = eval("self."+q).label()
					#print(id(eval("self.%s"%q)),id(eval("self.%s.__parent__"%q)),id(self),q,self.label(),type(eval("self.%s.__parent__"%q)))
					"""
					if (id(eval("self.%s.__parent__"%q))==id(self)) or 1==1:
						children[q] = eval("self."+q).label()
					else:
						children[q] = "%s <%d>" % (eval("self."+q).label(),id(eval("self."+q)))
					"""	
				else:		
					children[q] = repr(eval("self."+q))
			except Exception as ex:
				print(ex)
				children[q] = "Error: could not evaluate '%s' " %("self."+q)
		return children
		#return self.self.__attributes__()

	def __str__(self):
		return str(self.label())
		#return str(self.__attributes__())
		#return repr(self)

	def __repr__(self):
		#return str(self.toJSON())
		return "%s" %(self.label())
		#return "%s |%s|" %(self.label(),id(self))
		#return self

	def __bool__(self):
		return True	

	def span(self,child=None):
		if child is None: return self.__attributes__()
		tmp = []
		for attribute in self:
			tmp.append(attribute.eval("self."+child))
		return tmp	

		
		"""
		output = self.__attributes__()
		if len(output)==1:
			return str(output[0])
		return repr(output)
		"""


	def label(self):
		if self.__ID__:
			return self.__ID__
		return "<root>"	
		"""		
		if self.parent:
			for k,v in self.parent.__dict__.items():
				if id(v)==id(self):
					return k
			return "<root>"	
		"""

	def getroot(self):
		if self.__parent__:
			for k,v in self.__parent__.__dict__.items():
				if id(v)==id(self):
					higher = self.__parent__.getroot()
					if higher:
						return higher + "." + str(k)
					else:
						return "<root>." + str(k)
		return "<root>"	


	def getStuntman(self,parallelUniverse):
		path = self.getroot().split(".")[1:]
		root = parallelUniverse
		for child in path:
			root = getattr(root,child)
		return root	

	def __attributes__(self):
		return [k for k,v in self.__dict__.items()][3:]		

	def __children__(self):
		return [v for k,v in self.__dict__.items()][3:]		

	def __iter__(self):
		self.__current__ = 0
		return self
		#return self.__attributes__()[self.current-1]

	def __next__(self):
		#print(self.current)
		#print(self.__attributes__())
		if self.__current__ >= len(self.__attributes__()):
			#self.current = 0
			raise StopIteration
		else:
			self.__current__ += 1
			key = self.__attributes__()[self.__current__-1]
			#print(self.__dict__)
			#return key
			return self.__dict__[key]
			#return self.__attributes__()[self.current-1]	

	def __getitem__(self,obj):
		index = obj
		if isinstance(obj,ExclusionLogic):
			index = obj.label()
		if isinstance(index,str):
			for k,v in self.__dict__.items():
				#print(k,index)
				if k==index:
					return v	
			return DeepFalse()
		return self.__dict__.get(self.__attributes__()[index])

	def __deepcopy__(self,master):
		# Important steps here 
		# Avoids recursive for selfreferencing chains
		internalCopy =  master.get(id(self))
		if not internalCopy:
			internalCopy = ExclusionLogic(ID=self.label()) #NB! Parent saettes ved bornene
		master[id(self)] = internalCopy
		# The lines below are just creating
		# new objects for all new attributes
		# so never ending of selfreference
		# will fail
		#internalCopy = ExclusionLogic()	
		#master[id(internalCopy)] = internalCopy
		for k,v in self.__dict__.items():
			setattr(internalCopy, k, copy.deepcopy(v, master))
			obj = getattr(internalCopy, k)
			if isinstance(obj,ExclusionLogic):
				obj.parent = internalCopy  #NB!!! Her saettes parent til born
				#obj.ID = k
		return internalCopy	 

	def __getstate__(self):
		return current

	def __getattr__(self, name):
		"""Returns the attribute matching passed name."""
		# Get internal dict value matching name.
		value = self.__dict__.get(name)
		if not value:
			# Raise AttributeError if attribute value not found.
			if self.getroot():
				return DeepFalse(self.getroot()+"."+name)
			else:
				raise AttributeError("%s.%s is invalid."%(self.__class__.__name__,name))
		# Return attribute value.
		return value	

	def __len__(self):
		"""Returns the length of title."""
		return len(self.__attributes__())		

	def __contains__(self, key):
		return key in self.__attributes__()
		#return self.__dict__[key]

	"""
	def extend(self,key,obj=None):
		child = getattr(self,key)	
		if not child:
			child = ExclusionLogic(self,ID=key)
			setattr(self,key,child)
		if obj:
			child.add(obj)
		return child
	"""

	def __nextExclusionLogic__(self,key,unique=False):
		newExclusionLogic = self.__dict__.get(key)
		if not isinstance(newExclusionLogic,ExclusionLogic) or unique:
			newExclusionLogic = ExclusionLogic(parent=self,ID=key)
			setattr(self,key,newExclusionLogic)
		return newExclusionLogic	

	def __addExclusionLogicList__(self,key,alist):
		tmp = []
		for obj in alist:
			if isinstance(obj, ExclusionLogic):
				newEL = self.__nextExclusionLogic__(key)
				newEL.__addExclusionLogic__(obj)
				#newEL.set([obj.label()],obj)
				#if self.actors: print(self.actors.span())
				#setattr(self,key,obj)				
				#self.add({key:obj})
				#newEL.add({obj.label():obj})
			else:
				tmp.append(obj)
		if len(tmp)	> 0:
			setattr(self,key,tmp)

	def __addExclusionLogic__(self,exclusionlogic):
		if isinstance(exclusionlogic, ExclusionLogic):
			setattr(self,exclusionlogic.label(),exclusionlogic)
		else:	
			raise ExclusionLogicError("Error while adding a keyless %s to exclusionlogic %s:\n\t Objects of native types will needs to have a 'key' (string) in order to added to an Exclusion Logic object."%(type(exclusionlogic),self.label()))

	def __addfromList__(self,keys,value=True):
		if isinstance(keys,list):
			if len(keys)>2:
				newExclusionLogic = self.__nextExclusionLogic__(keys[0],unique=keys[1]=="!")
				newExclusionLogic.__addfromList__(keys[2:],value)
			else:
				if isinstance(value, ExclusionLogic):
					newExclusionLogic = self.__nextExclusionLogic__(keys[0],unique=keys[1]=="!")
					newExclusionLogic.__addExclusionLogic__(value)
				elif isinstance(value, list):
					self.__addExclusionLogicList__(keys[0],value)
				elif value is None:
					newExclusionLogic = self.__nextExclusionLogic__(keys[0],unique=keys[1]=="!")
				else:	
					# Adding any other type as final leaf
					setattr(self,keys[0],value)

	def __addfromDict__(self,dictionary,value=True):
		if isinstance(dictionary,dict):
			for key in dictionary.keys():
				if isinstance(dictionary[key],dict):
					newExclusionLogic = self.__nextExclusionLogic__(key)
					newExclusionLogic.__addfromDict__(dictionary[key],value)
				else:
					if isinstance(dictionary[key],list):
						self.__addExclusionLogicList__(key,dictionary[key])
					else:			
						# Adding any other type as final leaf
						setattr(self,key,dictionary[key])				
		else:
			self.__addExclusionLogic__(dictionary)

	def set(self,path,value=True):
		if isinstance(path,dict):
			self.__addfromDict__(path)
		elif isinstance(path,str):
			if path[-1] not in [".","!"]: path +="."
			path=re.split(r"([\.|\!]{1})+",path)[0:-1]
			#print(path)
			self.__addfromList__(path,value)
		elif isinstance(path,ExclusionLogic):
			self.__addExclusionLogic__(path)

	def add(self,dna,value=True):
		self.set(dna,value)

	"""		
	def add(self,dna,value=True):
		if isinstance(dna,dict):
			for key in dna.keys():
				if isinstance(dna[key],dict):
					newExclusionLogic = self.__nextEL__(key)
					newExclusionLogic.set(dna[key],value)
				else:
					if isinstance(dna[key],list):
						self.__addELfromList__(key,dna[key])
					else:			
						setattr(self,key,dna[key])				
		else:
			setattr(self,dna.label(),dna)					
	"""

	def pop(self,key):
		delattr(self,key)

	def expand(self,sentences):
		output = []

		tmp=[]
		for sentence in sentences:
			#regexpr = r'#{1}\[{1}([A-Za-z\.\!]*\([A-Za-z\.\!]+\)[A-Za-z\.\!]*)[{1}'
			regexpr = r'#\[(.*?)\]'
			counters = re.findall(regexpr,sentence)
			if len(counters)>0:
				#print("old sentence",sentence)
				#tmp=[]
				for counter in counters:
					#print(counter)
					res= self.expand([counter])
					number = len(res)
					sentence = sentence.replace("#["+counter+"]",str(number))
				#print("new sentence",sentence)
				tmp.append(sentence)
			else:
				tmp.append(sentence)
		#print("OLD:\t\t",sentences)			
		sentences=tmp
		#print("NEW:\t\t",sentences)			


		regexpr = r'([A-Z]+\([A-Za-z_\.\!]+\))+'
		params=[]
		for sentence in sentences:
			tmp = re.findall(regexpr,sentence)
			#print("tmp vars found:",tmp)
			params = list(set(params+tmp))
		combinations = [sentences]
		#print("params",params)

		for param in params:
			tmp = re.findall(r'\(([A-Za-z_\.\!]+)\)',param)
			#print("find core:",tmp)
			instances = eval(tmp[0])
			temp = []
			for combination in combinations:
				for instance in instances:
					treel = []
					for reel in combination:
						treel.append(reel.replace(param,instance))
					temp.append(treel)
			combinations=temp
		#print("combinations expanded",combinations)

		for combination in combinations:
			try:
				hh = eval(combination[0])
			except Exception as error:
				print("\n\n"+combination[0]+"\n\n")	
				print(combination)	
				raise ValueError('Represents a hidden bug, do not catch this') 
			if hh:
				output.append(combination)
			else:
				pass
				#print("Threw away:",combination[0])	
		return output			

	def eval(self,logical):
		return eval(logical)	

	"""
	def __setbackup__(self,dna,value=True):
		if isinstance(dna,dict):
			for key in dna.keys():
				if isinstance(dna[key],dict):
					newExclusionLogic = self.__dict__.get(key)
					#print(key,newExclusionLogic)
					if not isinstance(newExclusionLogic,ExclusionLogic):
						newExclusionLogic = ExclusionLogic(parent=self,ID=key)
						setattr(self,key,newExclusionLogic)
					newExclusionLogic.set(dna[key])
				else:
					setattr(self,key,dna[key])
		elif isinstance(dna,str):
			#print(dna)
			dna=dna.replace("self.","")
			if dna[-1]=="-":
				exec("self."+dna[:-2]+"-=1")
			else:	
				#print("  ",dna, end="",flush=True)
				dna=re.split(r"([\.|\!]{1})+",dna)
				#print(dna)
			#print(dna)
		if isinstance(dna,list):
			#print(dna)
			if len(dna)>1:
#				if hasattr(self,dna[0]):
				newExclusionLogic = self.__dict__.get(dna[0])
				#print(newExclusionLogic,dna[0],self.__dict__)
				if not isinstance(newExclusionLogic,ExclusionLogic) or dna[1]=="!":
					newExclusionLogic = ExclusionLogic(parent=self,ID=dna[0])
					setattr(self,dna[0],newExclusionLogic)
				newExclusionLogic.set(dna[2:])
			else:
				#print(dna[0])
				newExclusionLogic = self.__dict__.get(dna[0])
				if not isinstance(newExclusionLogic,ExclusionLogic):
					spike=re.split(r"([\=]{1})+",dna[0])
					if len(spike)==1:
						setattr(self,dna[0],True)
						#print("setting",dna[0])
					else:						
						setattr(self,spike[0],int(spike[2]))
	"""


class QuietError(Exception):
    # All who inherit me shall not traceback, but be spoken of cleanly
    pass

class ExclusionLogicError(QuietError):
	pass

def quiet_hook(kind, message, tb):
	if QuietError in kind.__bases__:
		print()
        #ex_type, ex, tb = sys.exc_info()
        #stack = traceback.extract_tb(tb)
    	#traceback.print_stack(f.f_back)
		#sys.__excepthook__(kind, message, tb.tb_next)
		cb = tb
		i=0

		while cb:
			cb= cb.tb_next
			i+=1

		traceback.print_tb(tb,limit=i-1)
		print('  {0}: {1}'.format(kind.__name__, message))  # Only print Error Type and Message
		#print(tb.tb_lasti)
	else:
		#print(kind.__bases__)
		sys.__excepthook__(kind, message, tb)  # Print Error Type, Message and Traceback

sys.excepthook = quiet_hook

def strlist(alist):
	if isinstance(alist,ExclusionLogic):
		alist = alist.span()
	if not isinstance(alist,list):
		alist = [alist]	
	output = ""
	for element in alist[:-2]:
		output += uncasted(element) + ", "
	if len(alist) > 1: output += uncasted(alist[-2]) + " and "
	if len(alist) > 0: 
		output += uncasted(alist[-1])
	else:
		output = "Nothing."
	return output
		
def uncasted(text):
	# We assume it's a noun
	# it's a name if Capital first
	if text[0].isupper(): return text
	# it's plural if ends on s
	if text[-1] == "s" : return "some "+text
	# definite singular if starts with a vocal
	if text[0] in ['a','e','i','u','o','y']:
		return "an "+text
	else:	
		return "a "+text

