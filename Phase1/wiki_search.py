#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
import re
import os
import sys
from nltk.corpus import stopwords
import Stemmer


# In[34]:


words = stopwords.words('english')
stopwords_dict = {}
for i in words:
    stopwords_dict[i] = 1
stemmer=Stemmer.Stemmer('english')


def process_query(query):
    parts=query.split(" ")
#     a=[]
#     categories=[]
    cat="NA"
    for word in parts:
        t = word.split(":")
        if(len(t) == 1):
            w = t[0].lower()
            try:
                stopwords_dict[w]
            except:
                s = stemmer.stemWord(w)
                components.append(s)
                categories.append(cat)
        else:
            w = t[1].lower()
            cat = t[0]
            try:
                stopwords_dict[w]
            except:
                s = stemmer.stemWord(w)
                components.append(s)
                categories.append(cat)
# for word in a:
# #     print(word)
#     for posting in postings:
#         if(posting.find("autism ")==0):
#             print(posting)ategories.append(cat)


# In[45]:


# query="i:2019 c:Cricket"
# a=[]
# categories=[]
# process_query(query)
# print(a)
# print(categories)

# for word in a:
# #     print(word)
#     for posting in postings:
#         if(posting.find("autism ")==0):
#             print(posting)
# In[19]:

#
# print(type(a))


# In[36]:


# file=open("../Index/invertinworddex.txt","rt")


# In[4]:


# postings=[]
# with open("../Index/invertindex.txt","rt") as file:
#     for lines in file:
#         postings.append(lines)
# Vijayraj

# In[5]:


# print(len(postings))AccessibleComputing

# In[15]:


# for word in a:
# #     print(word)
#     for posting in postings:
#         if(posting.find("autism ")==0):
#             print(posting)


# In[46]:

if __name__=="__main__":
    indexpath=sys.argv[1]
    query=sys.argv[2]
    # print(indexpath)
    # print(query)
    # print(type(query))

    components=[]
    categories=[]
    process_query(query)
    # print(components)
    # print(categories)
    postings=[]
    with open(indexpath+"index.txt","rt") as file:
        for lines in file:
            postings.append(lines)
    for i in range(len(components)):
        term=components[i]
        category=categories[i]
        for posting in postings:
            if(posting.find(term+" ")==0):
                if(category=="NA"):
                    print(posting)
                else:
#                 print("else")
                    breakout=posting.split()
#                 print(breakout)
                    if(breakout[1].find(category)!=-1):
                        print(posting)


# In[ ]:
