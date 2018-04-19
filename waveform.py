#!/usr/bin/env
import os,sys

WARNING_NO_FILE = "No score file specified."
WARNING_INVAID_PATH = "Invalid path to score file."
WARNING_UNKNOW = "Unknown source."
INS_DIR = "instruments"

global lstfile
global insdir
global charactor
global total

################################################################
# name:file name
# list:score list
class Score(object):
	def __init__(self, name):
		self.name = name
		self.rhythm=[]
		self.instrument=[]
		#self.result=[]
		return
		
	
	def add_rhythm(self,score) :				# input para |-*******************-|
		score = score[1:len(score)-1]		# delete the first and end char
		tmplst = []
		
		for c in score :
			if( c == '*' ) :
				tmplst.append(1)
			else :
				tmplst.append(0)
				
		self.rhythm.append( tmplst ) 
		return
		
	def parse_wave(self) :					# parse the wave of file(name=file name)
	
		f = open(insdir+"\\"+self.name,'r')
		tmplst = []
		for line in f.readlines() :      #y\t
			line = line.strip('\n');
			line = line.strip('\r');
			
			ls = line.split("\t");			
			
			if ( len(ls) >= 2 ):			
				y = int(ls[0])
				#line = line[t+1:len(line)]	# delete the tab and get new string
				#print(ls[1]);
				
				tmplst2 = []
				for c in ls[1] :
					if( c == ' ' ):
						tmplst2.append(0)
					else :
						tmplst2.append(y)
				
				tmplst.append(tmplst2)				   
		f.close()
		
		
		for t in tmplst :
			i = 0
			for t1 in t :
				#print t1,
				if ( len( self.instrument ) == i ) :
					self.instrument.append( t1 )
				else :
					self.instrument[i] += t1
				i+=1	
			#print ";"
		return
		
	def combination( self, instrument, rhythm ):  # combination instrument and rhythm
		lst = []
		idx = 0
		for x in rhythm :
			if(x==1) :
				lst.append(instrument[idx])
				idx += 1
			else :
				idx = 0				
				lst.append(instrument[idx])
		return lst
	
	def compost(self, lst):		# compost two or more lst
		result = []
		
		for ls in lst :
			idx = 0
			for ls2 in ls :
				if( len(result) == idx ) :
					result.append( ls2 )
				else :
					result[idx] += ls2
				idx += 1
				
		return result
	
	def parse_data(self):
		self.parse_wave()
		tmp = []
		for rm in self.rhythm :
			tmp.append( self.combination( self.instrument, rm ) )		
		self.result = self.compost( tmp )
		return
	
	def prints(self) :
		print self.name,":"
		print "instrument:",self.instrument
		print "rhythm:",
		for rm in self.rhythm :
			print rm
		print "result:",self.result
		return
#################################################################
# generate wave
def generateWave( lst ) :
	global charactor
	
	result = []
	
	
	maxi = max(lst)
	mini = min(lst)
	leni = len(lst)
	
	
	rows = maxi-mini+1
	cols = leni
	
	# inital data to space
	for i in range(rows) :
		ls = []
		for j in range(cols) :
			ls.append( ' ' )
		result.append( ls )
		
		
	prev = 'a'
	x = 0;
	for d in lst :
		y = d-mini
		if( prev == 'a' ) :
			result[y][x] = charactor
			prev = y
		else :
			if( prev > y+1 ) :   		#7->5 down
				for  y1 in range(y,prev+1) :
					result[y1][x] = charactor
			elif( prev+1 < y ) : #3->5 up
				for y1 in range(prev+1, y+1 ) :
					result[y1][x] = charactor
			else :
				result[y][x] = charactor
			prev = y		
		x += 1
		
	# Reversal and add the no
	n = mini
	for ls in result :
		head ="{:+2d}:\t".format(n)	
		idx = 0
		for c in head :
			ls.insert(idx,c)
			idx += 1
		n += 1
		
	result.reverse()
	
	for ls in result:
		for d in ls :
			print d,
		print ""
	
	return



#################################################################
def judgePara():

	global lstfile
	global insdir
	global total
	global charactor
	
	lstfile=[]
	charactor = '*'
	total = False
	
	if len(sys.argv) < 2 :
		print WARNING_NO_FILE
		return
		
	filedir = sys.path[0]			#the current script dir
	subdir = sys.argv[1]			#the para dir
	
	filepath = filedir+"\\"+subdir	
	insdir = filedir+"\\"+INS_DIR
	
	#print filepath
	
	if os.path.exists(filepath) == True and os.path.isdir(filepath) == True :
		lst = os.listdir(filepath)
		for name in lst :
			print name
			lstfile.append( filepath + "\\" + name )
	else :
		print WARNING_INVAID_PATH
		return	
		
	#discuss other parameter
	for i in range(2, len(sys.argv) ):
		para = sys.argv[i]
		if( para == "--total" ) :
			total = True
		if( para.find("--character=") != -1) :
			ls = para.split('=')
			charactor = ls[1][0]			
	return
	
####################################################
def disfile( filename ) :

	global total

	list = []
	f = open(filename,'r')
	for line in f.readlines() :   
		line = line.strip('\n');
		line = line.strip('\r');     
		if line[0]=='|' :     #last name add score
			list[ len(list)-1 ].add_rhythm(line)		
		else:									#add new score name			
			list.append( Score(line) )                      
	f.close()
	
	for obj in list :
		obj.parse_data()
		#obj.prints()
		if( total == False ):
			print( obj.name),":"
			generateWave( obj.result )
			
	if(total == True) :
		totalresult = []
		for obj in list :
			idx = 0
			for ls2 in obj.result :
				if( len(totalresult) == idx ) :
					totalresult.append( ls2 )
				else :
					totalresult[idx] += ls2
				idx += 1
		print( "Total:")
		generateWave( totalresult )
	
#####################################################


#####################################################
#main
print "*********************file list*****************"
judgePara()
print "*********************file list*****************"


for name in lstfile:
	print "@",name,"beign"
	disfile( name )
	print "####################################################################"

