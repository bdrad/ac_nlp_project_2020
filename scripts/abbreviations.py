## Functions to Solve Abbreviations

import pandas as pd
import re
from nltk import word_tokenize
from nltk.util import ngrams
import string



class AbbreviationSolver:
	def __init__(self,verbose=True, separate_solved_abbvs=False):
		self.verbose = verbose
		self.separate_solved_abbvs=separate_solved_abbvs
		self.abbv_df_fast = pd.read_csv('../resources/radiopedia_abbvs_v3.csv')

		# Load in stopwords from file
		self.stopwords = open('../resources/stopwords.txt','r').read().split('\n')


	# Adds full text and relevant abbreviations to expand search query
	#	abbv_f = abbreviation file
	#	Returns: Words and phrases expanding the search query
	# 	
	#	Optimized for speed, but cannot detect abbvs longer than 3 words and no reverse
	def solve_abbvs_fast(self,query):
		query = self.remove_stopwords(query)
		
		query_tkns = word_tokenize(query)

		query_tkns = [w.strip() for w in query_tkns if w.strip() not in string.punctuation and not w.strip().isspace()]

		query_tkns = query_tkns + [' '.join(x) for x in ngrams(query_tkns,2)] + [' '.join(x) for x in ngrams(query_tkns,3)]

		added_wrds = []

		# Iterate through abbreviation list to find any that are present
		abbv_lower_index = [x.lower() for x in self.abbv_df_fast.Abbreviation]
		for candidate in query_tkns:
			# print(candidate)
			if candidate in self.abbv_df_fast.Abbreviation and not self.abbv_df_fast[candidate]['Ambiguous']:
				if self.separate_solved_abbvs:
					added_wrds.append(self.abbv_df_fast[candidate].split(' '))
				else:
					added_wrds= added_wrds + self.abbv_df_fast[candidate].split(' ')
		
			elif candidate.lower() in abbv_lower_index:
				lowered_index = abbv_lower_index.index(candidate.lower())
				if not self.abbv_df_fast.iloc[lowered_index]['Case Sensitive'] and not self.abbv_df_fast.iloc[lowered_index]['Ambiguous']:
					if self.separate_solved_abbvs:
						added_wrds.append(self.abbv_df_fast.iloc[lowered_index]['Full Text'].split(' '))
					else:
						added_wrds= added_wrds + self.abbv_df_fast.iloc[lowered_index]['Full Text'].split(' ')
		
		if self.verbose:
			print('Solving the following abbvs: ',added_wrds)
			
		return added_wrds

	# Get user input about ambiguous abbreviation
	def request_abbv_clarif(self,abbv):
		print('\n')
		clarif = input('Please clarify "%s": ' % abbv)
		if clarif != '':
			return [clarif]
		else:
			return []

	# Remove stopwords from input
	# 	isArr: functionality for inputs of both one sentence string and tokenized sentence in array
	def remove_stopwords(self,input, isArr = False):
		if not isArr:
			doc = word_tokenize(input)
		else:
			doc = input
		output = [w for w in doc if w not in self.stopwords]
		if isArr:
			return output
		else:
			return ' '.join(output)