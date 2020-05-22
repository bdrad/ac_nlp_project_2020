import re
import math

# Returns the name of the narrative file from the numeric file name (e.g. 01_01.txt => Breast Cancer Screening)
def get_narr_name(fName, fPath = '../resources/criteria_links.txt'):
	f_name = fName.split('.')
	f_name = f_name[0].split('_')
	
	f_in = open(fPath, 'r', encoding ='utf8')
	mtch = re.search(r'Category '+f_name[0]+r':.+\n(\t.+\n)*?\tDisease '+f_name[1]+r': (.+)',f_in.read())
	f_in.close()
	if mtch:
		return(mtch.group(2))
	else:
		print(fName, 'You messed up in the narrative name!')
		return(None)

# Returns the category name of the numerically named file (e.g. 01_01.txt => Breast)
def get_cat_name(fName, fPath = '../resources/criteria_links.txt'):
	f_name = fName.split('.')
	f_name = f_name[0].split('_')
	
	f_in = open(fPath, 'r', encoding ='utf8')
	mtch = re.search(r'Category '+f_name[0]+r': (.+)\n(\t.+\n)*?\tDisease '+f_name[1]+r': (.+)',f_in.read())
	f_in.close()
	if mtch:
		return(mtch.group(1))
	else:
		print(fName, 'You messed up in the category name!')
		return(None)


# Print large arrays more cleanly for debugging
def pretty_print(myArr, order = []):
	if not order:
		for each in myArr:
			print('[',end='')
			for each2 in each:
				if isinstance(each2, float):
					print('%0.4f' % each2, end='\t')
				else:
					print(each2, end='\t')
			print(']')
	else:
		for each in myArr:
			print('[',end='')
			for ind in order:
				if isinstance(each[ind], float):
					print('%0.4f' % each[ind], end='\t')
				else:
					print(each[ind], end='\t')
			print(']')


# Function that weight large values more
def logis_tf(val, k=10):
	ret = 1/ (1 + math.exp(-k*(val - 0.5)))
	return ret