# -*- coding: utf-8 -*-
import os
if os.path.isfile("./output.txt"):
	os.remove("./output.txt")
import re
months = ["january","jan","february","feb","march","mar","april","apr","may","june","jun","july","jul","august","aug","september","sept","sep","october","oct","november","nov","december","dec"]
def isMonth(mon):
	mon = mon.lower()
	if mon in months:
		return 1
	else:
	 	return 0
def isYear(year):
	yea = re.compile(r"[0-9]{4}")
	if yea.match(year) is not None:
		return 1
	else: 
		return 0
def isDate(queryWords):
	iterVar = 0 
	day = re.compile(r"([0-2][0-9]|3[0-1])(st|nd|rd|th)?")
	length = len(queryWords)
	while(iterVar<len(queryWords)):
		outmonth,outyear = 0,0
		flagmonth=0
		if day.match(queryWords[iterVar]) is not None:
				if iterVar+1<length:	
					outmonth = isMonth(queryWords[iterVar+1])
					if outmonth==1:
						flagmonth = 1
				if iterVar+2<length and flagmonth!=0:
					outyear = isYear(queryWords[iterVar+2])
				if outmonth==1 and outyear==1:
					queryWords[iterVar] = queryWords[iterVar] +" " +queryWords[iterVar+1] +" " +queryWords[iterVar+2]
					del queryWords[iterVar+1]		
					del queryWords[iterVar+1]
				elif outmonth==1 and outyear==0:
					queryWords[iterVar] = queryWords[iterVar] + " "+queryWords[iterVar+1]
					del queryWords[iterVar+1]
		iterVar+=1
def tokenise(query):
	query = query + "\n" #remove this if reading from a file
	whiteSpaceCharacters = re.compile(u"[\s\u0020\u00a0\u0009]+",re.UNICODE)  #space,nbsp,tabspace
	query = whiteSpaceCharacters.sub(" ",query)

	#handle multiple new lines , replace them with single new line 
	query=re.sub(r"\n+","\n",query)


	#handle comma cases
	comma=re.compile(r"(. *)(,)( *.)")
	query = comma.sub(r"\g<1> \g<2> \g<3>",query)

	#handle dot cases (full stop)
	dot = re.compile(r"([a-z0-9] *)(\.)( *[^a-z0-9])")
	query = dot.sub(r"\g<1> . \g<3>",query)

	#handle contractions cases 
	contractions = re.compile(u"(\w+)(n['’′]t|['’′]ve|['’′]ll|['’′]d|['’′]re|['’′]s|['’′]m)",re.UNICODE)
	query = contractions.sub(r"\g<1> \g<2>",query)

	#handle hiphen cases 
	hiphen =  re.compile("(.)(- *\n *)(.)")
	query = hiphen.sub(r"\g<1>\g<3>",query)

	#handle colon cases
	colon = re.compile("([A-Za-z] *)(:)( *.)")
	query = colon.sub(r"\g<1> \g<2> \g<3>", query)

	#handle punctuation cases
	puncChars= ['"','**','|-','|','*','?','(',')','#','=',';','%','#','[',']','’','‘'] #: is removed
	for char in puncChars:
		query = query.replace(char," "+char+" ")
	queryWords = query.split()  #Split the entire list with space 
#	isDate(queryWords)  #check if date
	#final output
#	print "Final OUT = " ,queryWords
	foo = open("output.txt","a")
	for word in queryWords:
		foo.write(word+"\n")
	foo.close()


if __name__=="__main__":
#	query=" They're here. I am still standing there 12:30pm . I am complete. It's wither a|b. I am the M.P. My ip 127.0.0.1."
#query = "I'm akhil akkireddy, 13/12/2015    my   ip is 127.0.0.1:8080  akhil: akkireddy 13:14       31-12-2015  31.12.1201       [[birthday]] is on 13th april 1995."
	fo = open("input.txt","r")
	fileContent = fo.read()
	tokenise(fileContent)
