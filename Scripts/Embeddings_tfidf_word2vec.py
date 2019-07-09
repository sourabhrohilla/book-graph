#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[8]:


dataset = pd.read_csv("/home/karan/dataset.csv",encoding="ISO-8859-1")


# In[20]:


import nltk
import string
import re

nltk.download('stopwords')


# In[22]:


#REMOVING STOPWORDS AND CONVERTING IN LOWERCASE
def remove_stopwords(row):
    article = row['Summary']
    article = article.lower()
    stopwords = set(nltk.corpus.stopwords.words('english') + ['reuter', '\x03'])
    articles = [word for word in article.split() if word not in stopwords]
    return " ".join(articles)


# In[23]:


#REMOVE PUNCUATIONS
def remove_puc(row):
    article = row['Summary_custom']
    #REPLACE PUNCTUATIONS WITH SPACE
    articles = re.sub(r"[,.;@#?!&$-:/]+", ' ', article)
    #REPLACE NUMBERS WITH SPACE
    articles = re.sub(r'\d+', ' ', articles)
    return articles


# In[24]:


#STEMMING
stemmer = nltk.stem.PorterStemmer()
def stemming(row):
    article = row['Summary_custom']
    article = article.split()
    articles = " ".join([stemmer.stem(word) for word in article])
    return articles


# In[25]:


dataset['Summary_custom'] = dataset.apply(remove_stopwords,axis=1)
# dataset['Summary_custom'] = dataset.apply(stemming,axis=1)
dataset['Summary_custom'] = dataset.apply(remove_puc,axis=1)


# In[28]:


#TRY FITTING MODEL WITH TFIDF FIRST, THEN GO ON WITH MORE COMPLEX ALGOS
#IF WE DONT PROVIDE VOCAB, IT WILL MAKE FROM EXISTING COLUMN.
import sklearn
counter = sklearn.feature_extraction.text.CountVectorizer()
bag_of_words = counter.fit_transform(dataset['Summary_custom'])
tf_counter = sklearn.feature_extraction.text.TfidfVectorizer()
tfidf = tf_counter.fit_transform(dataset['Summary_custom'])


# In[30]:


vocab = counter.get_feature_names()


# In[33]:


import numpy as np
from gensim.models import Word2Vec
model = Word2Vec([vocab], min_count=1)
matrix = []
for word in vocab:
    matrix.append(model[word])
wordvec_matrix = np.array(matrix)


# In[34]:


wordvec_matrix.shape


# In[35]:


docvec_mat = tfidf.dot(wordvec_matrix)


# In[36]:


docvec_mat.shape


# In[ ]:




