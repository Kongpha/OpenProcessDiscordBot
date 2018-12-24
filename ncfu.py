from enum import Enum
import random
import copy

#c = ["b", "c", "d","f","g","h","l","m","n","p","q","r","s","t","v","w","y","z"]
#C = ["b", "c", "ch", "d", "f", "g", "gh", "j", "k", "l", "llr", "m", "n", "nn", "p", "ph", "phpr", "q", "qu", "r", "rt", "rtm", "s", "sh", "t", "th", "v", "vm", "w", "wh", "y", "z"]
#B = ["b", "bl", "br", "c", "ch", "chr", "cl", "cr", "d", "dr", "f", "g","h", "j", "k", "l", "ll", "m", "n", "p", "ph", "qu", "r", "rh", "s","sch", "sh", "sl", "sm", "sn", "st", "str", "sw", "t", "th", "thr","tr", "v", "w", "wh", "y", "z", "zh"]
#v = ["a", "e", "i", "o", "u", "y"]
#V = ["a", "e", "i", "o", "u", "y", "ae", "ai", "au", "ay", "ea", "ee", "ei", "eu", "ey", "ia", "ie", "oe", "oi", "oo", "ou", "ui"]
#s = ["b", "d", "f", "g", "h", "k", "l", "m", "n", "p", "r", "s", "t", "v", "w", "x", "y"]
#vS = ["ch", "ck", "rd", "ge", "ld", "le", "", "ang", "ar", "ard", "as", "ash", "at", "ath", "augh", "aw", "ban", "bel", "bur", "cer","cha", "che", "dan", "dar", "del", "den", "dra", "dyn", "ech", "eld","elm", "em", "en", "end", "eng", "enth", "er", "ess", "est", "et","gar", "gha", "hat", "hin", "hon", "ia", "ight", "ild", "im", "ina","ine", "ing", "ir", "is", "iss", "it", "kal", "kel", "kim", "kin", "ler", "lor", "lye", "mor", "mos", "nal", "ny", "nys", "old", "om","on", "or", "orm", "os", "ough", "per", "pol", "qua", "que", "rad","rak", "ran", "ray", "ril", "ris", "rod", "roth", "ryn", "sam","say", "ser", "shy", "skel", "sul", "tai", "tan", "tas", "ther","tia", "tin", "ton", "tor", "tur", "um", "und", "unt", "urn", "usk","ust", "ver", "ves", "vor", "war", "wor", "yer"]
#S = ["ch", "ck", "rd", "ge", "ld", "le", "ng", "sh", "th", "gh","ne", "ke", "mp", "ft", "mb", "dt", "ph", "rt", "pt", "mn","nth", "dth", "rth", "mph", "rph", "nph", "st", "sh", "sk","yth", "ythm", "yn", "yh", "lt", "ll", "rn"]

symbols = [["c",["b", "c", "d","f","g","h","l","m","n","p","q","r","s","t","v","w","y","z"]],["C",["b", "c", "ch", "d", "f", "g", "gh", "j", "k", "l", "llr", "m", "n", "nn", "p", "ph", "phpr", "q", "qu", "r", "rt", "rtm", "s", "sh", "t", "th", "v", "vm", "w", "wh", "y", "z"]],["B",["b", "bl", "br", "c", "ch", "chr", "cl", "cr", "d", "dr", "f", "g","h", "j", "k", "l", "ll", "m", "n", "p", "ph", "qu", "r", "rh", "s","sch", "sh", "sl", "sm", "sn", "st", "str", "sw", "t", "th", "thr","tr", "v", "w", "wh", "y", "z", "zh"]],["v",["a", "e", "i", "o", "u", "y"]],["V",["a", "e", "i", "o", "u", "y", "ae", "ai", "au", "ay", "ea", "ee", "ei", "eu", "ey", "ia", "ie", "oe", "oi", "oo", "ou", "ui"]],["s",["b", "d", "f", "g", "h", "k", "l", "m", "n", "p", "r", "s", "t", "v", "w", "x", "y"]],["vS",["ch", "ck", "rd", "ge", "ld", "le", "", "ang", "ar", "ard", "as", "ash", "at", "ath", "augh", "aw", "ban", "bel", "bur", "cer","cha", "che", "dan", "dar", "del", "den", "dra", "dyn", "ech", "eld","elm", "em", "en", "end", "eng", "enth", "er", "ess", "est", "et","gar", "gha", "hat", "hin", "hon", "ia", "ight", "ild", "im", "ina","ine", "ing", "ir", "is", "iss", "it", "kal", "kel", "kim", "kin", "ler", "lor", "lye", "mor", "mos", "nal", "ny", "nys", "old", "om","on", "or", "orm", "os", "ough", "per", "pol", "qua", "que", "rad","rak", "ran", "ray", "ril", "ris", "rod", "roth", "ryn", "sam","say", "ser", "shy", "skel", "sul", "tai", "tan", "tas", "ther","tia", "tin", "ton", "tor", "tur", "um", "und", "unt", "urn", "usk","ust", "ver", "ves", "vor", "war", "wor", "yer"]],["S",["ch", "ck", "rd", "ge", "ld", "le", "ng", "sh", "th", "gh","ne", "ke", "mp", "ft", "mb", "dt", "ph", "rt", "pt", "mn","nth", "dth", "rth", "mph", "rph", "nph", "st", "sh", "sk","yth", "ythm", "yn", "yh", "lt", "ll", "rn"]]]

mons_std = "[cham|chan|jisk|lis|frich|isk|lass|mind|sond|sund|ass|chad|lirt|und|mar|lis|il|gil|est|sel|[<B>|<V>|<S>]][jask|ast|ista|adar|irra|im|ossa|assa|osia|ilsa|ata|gara|ara|[<v>|<v>|<C>]][|[an|ya|la|sta|nya|proc|ator|rator|yator|nisk|ta|ma|resc|ety|shilly|mal|sal|tal|nal|lock|lloc|llock|nite|tite|mite|site|dite|to|no|mo|to|reon|leon]]"

class groupType(Enum) :
	tstr = 1
	tsye = 2
	tsya = 3
	trvs = 4
	trsw = 5
	tstt = 0
class group :
	def __init__(self):
		self.type = groupType.tstt
		self.storage = []
		self.result = 'null'

	def randomAll(self) :
		if self.storage :
			#print("RANDOM")
			#print(self.storage)
			self.result = random.choice(self.storage)
			self.type = groupType.tstt
	def randomSymbolAll(self) :
		if self.storage :
			for x in self.storage : # x = C, V, S
				for y in symbols : # y = ["C",[...]]
					if x == y[0] :
						self.result = random.choice(y[1])
						break
					else :
						self.result = "null"
					self.type = groupType.tstt
		

#print(parse_nested(temp))



def throwerror(msg) :
    raise ValueError('error : '+msg)
def n_t_generate(strr) :
	tempp = copy.deepcopy(strr)
	currfloor = 0
	avoidsp = False
	textmem = ""
	resultf = ""
	tempstack = []
	tempgroup = group()
	blocklt = []
	stack = []
	tempp += " "

#def addPerv() :
#	tempgroup.type = groupType.tstt
#	tempgroup.storage.clear()
#	tempgroup.storage.append(textmem)
#	tempgroup.result = textmem
#	stack.append(tempgroup.result)
#	tempgroup.storage.clear()
#	textmem = ""

	for ind, ch in enumerate(tempp) :
		if ind == len(tempp) - 1 :
			if currfloor != 0 :
				throwerror('Stack Error')
			else :
				tempgroup.type = groupType.tstt
				tempgroup.storage.clear()
				tempgroup.storage.append(textmem)
				tempgroup.result = textmem
				stack.append(tempgroup.result)
				tempgroup.storage.clear()
				textmem = ""
		if ch == '[' :
			tempstack.append(group())
			blocklt.append(groupType.tstt)
			#print([cll.storage for cll in tempstack])
			if currfloor == 0 :
				tempgroup.type = groupType.tstt
				tempgroup.storage.clear()
				tempgroup.storage.append(textmem)
				tempgroup.result = textmem
				stack.append(tempgroup.result)
				tempgroup.storage.clear()
				textmem = ""
		
			currfloor += 1
		elif ch == '<' :
			tempstack.append(group())
			blocklt.append(groupType.tstr)
			if currfloor == 0 :
				tempgroup.type = groupType.tstt
				tempgroup.storage.clear()
				tempgroup.storage.append(textmem)
				tempgroup.result = textmem
				stack.append(tempgroup.result)
				tempgroup.storage.clear()
				textmem = ""
			currfloor += 1
		elif ch == ']' :
			if currfloor == 0 or blocklt[-1] != groupType.tstt:
				throwerror('Stack Error')
			else :
				#tempstack[currfloor-1].storage.clear()
				if textmem != "" :
					tempstack[currfloor-1].storage.append(textmem)
					textmem = ""	
				#tempstack[currfloor-1].storage = tempstack
				tempstack[currfloor-1].randomAll()
				#print(">>> HAVE")
				#print("")
				#print("")
				if currfloor > 1 :
					tempstack[currfloor-2].storage.append(tempstack[currfloor-1].result)
				else :
					stack.append(tempstack[currfloor-1].result)
				#print(stack)
				currfloor -= 1
				#attrs = [vars(cll) for cll in stack]
				#tempgroup.storage.clear()
				tempstack.pop()
				blocklt.pop()
		elif ch == '>' :
			if currfloor == 0 or blocklt[len(blocklt)-1] != groupType.tstr:
				throwerror('Stack Error')
			else :
				#print(tempstack[currfloor-1])
			
				#tempstack[currfloor-1].storage.clear()
				if textmem != "" :
					tempstack[currfloor-1].storage.append(textmem)
					textmem = ""	
				#tempstack[currfloor-1].storage = tempstack
				tempstack[currfloor-1].randomSymbolAll()
				if currfloor > 1 :
					tempstack[currfloor-2].storage.append(tempstack[currfloor-1].result)
				else :
					stack.append(tempstack[currfloor-1].result)
				#print(stack)
				currfloor -= 1
				#attrs = [vars(cll) for cll in stack]
				#tempgroup.storage.clear()
				tempstack.pop()
				blocklt.pop()
		elif ch == '|' :

			tempstack[currfloor-1].storage.append(textmem)
			#print([vars(cll) for cll in tempstack])
			#print(tempstack[currfloor-1].storage)
			textmem = ""
		else :
			textmem += ch
			#print(textmem)

	for cll in stack :
		resultf += cll
	return resultf