## Functions to process intitial query

from abbreviations import AbbreviationSolver
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
import string




class Preprocess:

	def __init__(self, want_ngrams=True, verbose=True, fast=False, separate_solved_abbvs=False):
		self.want_ngrams = want_ngrams
		self.verbose = verbose
		self.fast = fast
		
		self.separate_solved_abbvs = separate_solved_abbvs

		self.abbv_solver = AbbreviationSolver(self.verbose, self.separate_solved_abbvs)
		
		self.stopwords = open('../resources/stopwords.txt','r').read().split('\n')
		self.lemmatizer = WordNetLemmatizer() 

	# INITIAL/PRIMARY input processing method
	#   1. Preprocess query, remove stopwords
	#   2. Add 2 and 3 word nGrams, expand query (optional)
	#   3. Solve Abbreviations, expand query
	#   4. Remove any added stopwords
	#   Returns: tokenized words and phrases
	def process_query(self,query):
		print('VERBOSE:', self.verbose)
		if self.fast:
			fltr_tkns = self.preprocess(query)
		else:
			fltr_tkns = self.preprocess(query)

		# Make 2 and 3 words ngrams of words to make high-value matches to terms
		if self.want_ngrams:
			ngram_tkns = [' '.join(ng) for ng in ngrams(fltr_tkns,2)] + [' '.join(ng) for ng in ngrams(fltr_tkns,3)]
			fltr_tkns = fltr_tkns + ngram_tkns
			if self.verbose:
				print('NGrams Added:', ngram_tkns)

		# Add abbreviations and full-forms to the query
		abv_words = []
		if self.fast:
			abv_words = self.abbv_solver.solve_abbvs_fast(query)
		else:
			abv_words = self.abbv_solver.solve_abbvs(query)

		print('ABV', abv_words)
		print('FLTR', fltr_tkns)
		if self.separate_solved_abbvs:	
			fltr_tkns = [fltr_tkns]  + abv_words
		else:
			fltr_tkns = fltr_tkns + abv_words
		
		if self.verbose:
			print('Abbreviations solved:', abv_words)

		# fltr_tkns = remove_duplicates(fltr_tkns)
		# fltr_tkns = remove_stopwords(fltr_tkns, True)

		if self.verbose:
			print('Final Query:',fltr_tkns)

		return fltr_tkns

	# Processes text by lowering it, splitting into tokens, removing stopwords, numbers, and punctuation, 
	# and finally lemmatizing.
	def preprocess(self,doc):
		doc = doc.lower()  # Lower the text.
		doc = word_tokenize(doc)  # Split into words.
		doc = [w for w in doc if w not in self.stopwords]  # Remove stopwords.

		# Remove numbers and punctuation, and lemmatizes. PROBLEMATIC with '/' abbreviations! 
		doc = [self.lemmatizer.lemmatize(w) for w in doc if w.isalpha()] #not in string.punctuation and not w.isnumeric()]  
		return doc

	# Processes text by lowering it, splitting into tokens, removing stopwords, numbers, and punctuation, 
	# and finally lemmatizing.
	def preprocess_fast(self,doc):
		doc = doc.lower()  # Lower the text.
		doc = word_tokenize(doc)  # Split into words.
		doc = [w for w in doc if w not in self.stopwords]  # Remove stopwords.

		# Remove numbers and punctuation, and lemmatizes. PROBLEMATIC with '/' abbreviations! 
		doc = [w for w in doc if w.isalpha()] #not in string.punctuation and not w.isnumeric()]  
		return doc

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

	# Removes duplicates in list while preserving order
	def remove_duplicates(self,my_list):
		seen = set()
		result = []
		for item in my_list:
			if item not in seen:
				seen.add(item)
				result.append(item)
		return result

