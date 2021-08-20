# ACR Appropratiness Criteria (AC) NLP Search Tool
### Repository to accompany manuscript

## Purpose
Our study developed and evaluated a search and match natural language processing tool for selecting evidence-based radiology studies in the American College of Radiology (ACR) Appropriateness Criteria (AC) using patient clinical indications and demographics. The AC is underutilized by clinicians, resulting in less evidence-based care. We aim to increase use by developing an efficient, clinician-centered web app that can match clinical indications to AC documents and variants.

## Instructions for Running Locally
1. `pip install requirements.txt`
1. Gather additional requirements (see below)
1. Run `process_artificial_inds.ipynb` jupyter notebook

## Additional requirements
* Embeddings: our model has similar embeddings to publically availabe ones [here](https://ftp.ncbi.nlm.nih.gov/pub/lu/Suppl/BioSentVec/BioSentVec_PubMed_MIMICIII-bigram_d700.bin). 
* Word2int and Vocab files: These were too large to include in this repository, and can be substituted with those extracted from the above public model using a modified sent2vec implementation (/sent2vec-master-edited).

## Acknowledgements
We are grateful to the developers of fasttext, sent2vec, and BioSentVec for making their software and dataset available publically.

