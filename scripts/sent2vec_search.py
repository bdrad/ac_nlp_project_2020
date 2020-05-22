## Implementation that uses sent2vec to better semantically match a query to a document
## Uses the same preprocessing and weighting as tfidf_embeddings

import numpy as np
import os
import traceback
import re
from string import punctuation
from scipy.spatial import distance
import sys

from preprocess import Preprocess
from util_fxns import get_narr_name, logis_tf, pretty_print
from weight_score import weight_file
from query_user_input import get_user_input, process_input

from boto3.dynamodb.conditions import Key, Attr

import ctypes
import numpy as np
import csv
import requests

class Sent2VecSearch:

	def __init__(self,vocab,word2int,names, docs_embed, headers_embed, tfidf_embed, verbose=True, model=None, table=None):
		self.vocab = vocab
		self.word2int = word2int
		self.names = names
		self.docs_embed = docs_embed
		self.headers_embed = headers_embed
		self.tfidf_embed = tfidf_embed
		self.verbose = verbose
		self.model = model
		self.table = table
		self.preprocessor = Preprocess(want_ngrams=False, verbose=True, fast=True, separate_solved_abbvs=True)


	def embed_sentence(self,tkn_wrds):
		inds = self.getAllIndices(tkn_wrds)
		print('inds: ',inds)
		embeds = np.zeros(350,dtype=float)
		added_wrd_ct = 0
		for ii,each_ind in enumerate(inds):
			if int(each_ind) != -1:

				response = self.table.query( KeyConditionExpression=Key('h_index').eq(int(each_ind)) )

				if len(response['Items']) > 1:
					print('Uh oh you have too many items: ',len(response['Items']))
					input()

				if len(response['Items']) == 1:
					resp_arr = np.array(response['Items'][0]['embeds']).astype(np.float)
					embeds = np.add(embeds,resp_arr)
					added_wrd_ct += 1
				else:
					print("Word not added to dict")
			else:
				print("Word was not found: ",tkn_wrds[ii])

		if added_wrd_ct >0:
			embeds = embeds/added_wrd_ct

		print(len(embeds))
		return embeds

	# query will have 0: indications, 1: age, 2: sex, 3: body part; value can be ''
	def search(self,query_list):

		results = []

		try:
			[query, q_age, q_sex, q_bodypart] = process_input(query_list)

			final_query = self.preprocessor.process_query(query)

			sent_vec = np.zeros(350,dtype=float)
			if len(final_query)>0:
				if self.model:
					print('Encoding: ', ' '.join(final_query[0]))
					sent_vec = self.model.embed_sentence(' '.join(final_query[0]))[0]
				else:
					sent_vec = self.embed_sentence(final_query[0]) #will always be query
				for ii in range(1,len(final_query)): # only if abbvs
					if len(final_query[ii]) > 0:
						weight = len(final_query[ii])/(len(final_query[0]) + len(final_query[ii]))
						print('embedding: ',final_query[ii], weight)
						this_vec = np.zeros(350,dtype=float)
						if self.model:
							print('Encoding: ', ' '.join(final_query[0]))
							this_vec = self.model.embed_sentence(' '.join(final_query[ii]))[0]
						else:
							this_vec = self.embed_sentence(final_query[ii])

						sent_vec = np.add(sent_vec, weight*this_vec)


			# print('sentvec: ',sent_vec)
			sims_list = []

			for i in range(len(self.docs_embed)):

				[b_part_weight, pediatric_weight, sex_weight] = weight_file(self.names[i], q_bodypart, q_age, q_sex)

				# Calculate score based on query similarity to full narrative + similarity to headers
				score_doc = 1 - distance.cosine(sent_vec, self.docs_embed[i])
				score_head = 1 - distance.cosine(sent_vec, self.headers_embed[i])
				score_tf = 1 - distance.cosine(sent_vec, self.tfidf_embed[i])


				score_doc = score_doc * b_part_weight * pediatric_weight * sex_weight
				score_head = score_head * b_part_weight * pediatric_weight * sex_weight
				score_tf = score_tf * b_part_weight * pediatric_weight * sex_weight

				score = score_doc + score_head + score_tf

				sims_list.append([get_narr_name(self.names[i]), self.names[i], score_doc, score_head, score_tf, score, i])

				# if self.verbose:
				# 	# print(i,len(names),len(sims_list))
				# 	print(self.names[i], 'cosine similarity:', sims_list[i][2])

			srted_sims = sorted(sims_list, key= lambda x:x[5],reverse=True)

			# ct = 0
			# ind = 0
			# results = []
			# while ct <30:
			# 	if srted_sims[ind][0] != srted_sims[ind+1][0]:
			# 		if self.verbose:
			# 			print(ct+1,':',srted_sims[ind])
			# 		results.append([ srted_sims[ind][6], srted_sims[ind][0], srted_sims[ind][1] ]) #i, narr_name, f_name
			# 		ct += 1
			# 	ind+=1
			results = srted_sims

		except Exception as e:
			traceback.print_exc()
			results = [[0,"Error", "thrown"],[1,"Error", "thrown"]]
			final_query = [[''],['']]

		return results


	def hash(self,word):
		m1 = 2166136261
		m2 = 16777619
		h = m1
		h=np.uint32(m1)
		m2 = np.uint32(m2)
		for each in word:
			h = np.bitwise_xor(h,np.uint32(ord(each)))
			h = h * m2
		return h

	def getIndex(self,word):
		MAX_VOCAB_SIZE = 30000000

		h = self.hash(word) % MAX_VOCAB_SIZE


		while (self.word2int[h] != -1 and self.vocab[self.word2int[h]] != word):
			print(word, 'not in dict!')
			h = (h + 1) % MAX_VOCAB_SIZE

		print('index fxn', h, word, self.vocab[self.word2int[h]])
		return self.word2int[h]

	def getNgrams(self,wrd_inds, ngram_len = 2):
		m3 = 116049371
		bucket = 2000000
		max_v = 3002889

		ngrams = []
		for ii in range(len(wrd_inds)- ngram_len +1):
			ind = wrd_inds[ii]
			for jj in range(ii+1,ii + ngram_len):
				ind = ctypes.c_uint64(ind * m3 + wrd_inds[jj]).value
				ngrams.append(max_v + (ind % bucket))
		print('ngrams: ', ngrams)
		return ngrams

	def getAllIndices(self,tk_sent):
		indices = []

		for word in tk_sent:
			indices.append(self.getIndex(word))

		print('O indices:', indices)
		indices = indices + self.getNgrams(indices)

		return indices
