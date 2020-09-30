#!/usr/bin/env python
# coding: utf-8

# In[432]:


import nltk
import re
import os
import sys
from nltk.corpus import stopwords
from datetime import datetime
import Stemmer
import unicodedata
import time
import math
import operator


# In[477]:


map_fields = { "t":0 , "x":1 , "i":2 , "c":3 , "l":4 , "r":5}
reverse_fields = { "0":"t" , "1":"x" , "2":"i" , "3":"c" , "4":"l" , "5":"r"}
mp = { "t":"t" , "b":"x" , "i":"i" , "c":"c" , "l":"l" , "r":"r"}
map_weight = { "0":100 , "1":10 , "2":5 , "3":5 , "4":0.75 , "5":0.75}


# In[434]:


splitdir="../Split/"
titledir="../Title/"
stopwords_dict={}
stemmer=Stemmer.Stemmer('english')
K=0
a=[]
categories=[]


# In[435]:


topfilecontents=open(splitdir+"top").readlines()


# In[436]:


totaldocs=open("../Index/MyTitle").readlines()
# print(len(totaldocs))


# In[437]:


N=len(totaldocs)


# In[438]:


def getStopWords():
    stopWords=stopwords.words('english')
    additionalwords=["ref","/ref","references","reflist"]
    global stopwords_dict
    for word in additionalwords:
        stopWords.append(word)
    for word in stopWords:
        stopwords_dict[word]=1


# In[439]:


def process_query(query):
    global K
    global a
    global categories
    parts=query.split(" ")
    K=int(parts[0].split(",")[0])
    parts.pop(0)
    cat="NA"
    for word1 in parts:
        t = word1.split(":")
        if(len(t) == 1):
            word = t[0].lower()
            try:
                stopwords_dict[word]
            except:
                s = stemmer.stemWord(word)
                a.append(s)
                categories.append(cat)
        else:
            word = t[1].lower()
            cat = t[0]
            try:
                stopwords_dict[word]
            except:
                s = stemmer.stemWord(word)
                a.append(s)
                categories.append(cat)


# In[440]:


# a=[]
# categories=[]
# process_query("3, sachin tendulkar")


# In[441]:


# print(K)


# In[442]:


# print(a)


# In[443]:


# print(categories)


# In[444]:


# def find_file(word):
#     searchlines=topfilecontents
#     if(searchlines[0].find("NL")!= -1):
#         line=0
#         while(line<len(searchlines)-1):
#             tmp=searchlines[line].split()
#             if(tmp[0]<=word and searchlines[line+1].split()[0]>word):
#                 print(tmp[1])
#                 break
#             line+=1
#         if(line==len(searchlines)-1):
#             print(searchlines[line].split()[1])



# In[445]:


# find_file("autism")


# In[446]:


# print(topfilecontents)


# In[447]:


# Index_lines = open(splitdir + "L17.0").readlines()


# In[448]:


# print(Index_lines)


# In[449]:


# print(len(Index_lines))


# In[450]:


def binary_search(searchlines,word,start,end):
#     print("binary search")
#     print(start)
#     print(end)
    if(start>end):
        return "Not found"
    mid=int((start+end)/2)
#     print(mid)
    tmp1=searchlines[mid].split()
    if(word < tmp1[0]):
        return binary_search(searchlines,word,start,mid-1)
    elif(word > tmp1[0]):
        return binary_search(searchlines,word,mid+1,end)
    else:
        return tmp1[1]


# In[451]:


def find_file(word,startfile):
    searchlines=startfile
    #we start with the top file which is our root
    #Since the content is ordered, we keep on
    while(searchlines[0].find("NL")!= -1):
        line=0
        while(line<len(searchlines)-1):
            tmp=searchlines[line].split()
            if(tmp[0]<=word and searchlines[line+1].split()[0]>word):
                try:
                    searchlines=open(splitdir+tmp[1]).readlines()
                    break
                except:
                    return "Not found"
            line+=1
        if(line==len(searchlines)-1):
            try:
                searchlines=open(splitdir+searchlines[line].split()[1]).readlines()
            except:
                return "Not found"
#     print(tmp)
    #searchlines now has contents of the target file
    #do binary search to get it.
#     print(searchlines)
    tmp=binary_search(searchlines,word,0,len(searchlines)-1)
    return tmp




# In[452]:


# y=find_file("autism")


# In[453]:


# l=open(splitdir+'16220.0').readlines()


# In[454]:


# # print(l)
# # print(y)
# ty=y.split("|")
# print(ty)


# In[455]:


# ty[-1]=ty[-1][:-1]


# In[456]:


# print(ty)


# In[457]:


def getdocID(doc):
    docID=""
    l=""
    f=0
    count_list=[]
    for d in doc:
        if(d.islower()):
            f=1
        if(f==0):
            docID+=d
        else:
            if(d.isalpha()):
                l+=" "+d+" "
            else:
                l+=d
    count_list=[0,0,0,0,0,0]
    l=l[1:]
    splitl=l.split()
    j=0
    while(j<len(splitl)):
        count_list[map_fields[splitl[j]]]+=int(splitl[j+1])
        j+=2
    return [docID,count_list]



# In[458]:


def RankDox():
    rank_docs={}
    for i in range(len(query_words)):
        # print(query_words[i])
        postlist=find_file(query_words[i],topfilecontents)
        if(postlist!="Not Found"):
            postlist=postlist.split("|")
            # print(postlist)
#             postlist[-1]=postlist[-1][:-1]
            doc_freq={}
            term_freq=0
            for segment in postlist:
                try:
                    tmp=getdocID(segment)
                except:
                    continue
                # print(tmp)
                doc_freq[tmp[0]]=tmp[1]
                term_freq+=1
            for doc in doc_freq:
                wt=0
                for field in range(len(doc_freq[doc])):
                    if(categories[i]=='NA'):
                        wt+=doc_freq[doc][field]*map_weight[str(field)]*math.log(N/(term_freq*1.0))
                    else:
                        if(mp[categories[i]]==reverse_fields[str(field)]):
                            wt+=doc_freq[doc][field]*map_weight[str(field)]*math.log(N/(term_freq*1.0))
                try:
                    rank_docs[doc]+=wt
                except:
                    rank_docs[doc]=wt
    try:
        return rank_docs
    except:
        return -1





# In[459]:


# query_words=a


# In[460]:


# print(query_words)


# In[461]:


N=9828414


# In[462]:


# rd=RankDox()


# In[463]:


# print(len(rd))


# In[464]:


# print(rd)


# In[465]:


def binary_search_title(searchlines,id,start,end):
    if(start>end):
        return None
    mid=int((start+end)/2)
    tmp=searchlines[mid].split(" ",1)
    if(int(id)>int(tmp[0])):
        return binary_search_title(searchlines,id,mid+1,end)
    elif(int(id)<int(tmp[0])):
        return binary_search_title(searchlines,id,start,mid-1)
    else:
        return tmp[1]


def find_file_title(docid,startfile):
    searchlines=startfile
#     print('----------')
    while(searchlines[0].find("NL")!=-1):
        line=0
        while(line<(len(searchlines)-1)):
            tmp=searchlines[line].split()
#             print(tmp[0])
#             print(docid)
#             print(searchlines[line+1].split()[0])
#             print(tmp[0])

            if(int(tmp[0]) <= int(docid) and int(searchlines[line+1].split()[0]) > int(docid)):
#                 print(titledir+tmp[1])
                searchlines=open(titledir+tmp[1]).readlines()
                break
            line+=1
        if(line==(len(searchlines)-1)):
            searchlines=open(titledir+searchlines[line].split()[1]).readlines()

    tmp=binary_search_title(searchlines,docid,0,len(searchlines)-1)
    return tmp




# In[466]:


# query="3, autism"
# a=[]
# categories=[]
# process_query(query)


# In[467]:


# print(a)


# In[468]:


# categories


# In[469]:


# query_words=a


# In[470]:


# start=datetime.now()
# rd=RankDox()
# end=datetime.now()
# print(end-start)


# In[471]:


# print(rd)


# In[472]:


# if(rd!=-1):
# #     print('if')
#     toptitlecontents=open(titledir+"top").readlines()
#     sorted_rd=sorted(rd.items(),key=operator.itemgetter(1),reverse=True)
#     if(len(sorted_rd)==0):
#         print("Sorry No matches")
#     else:
#         count=0
#         for i in range(len(sorted_rd)):
#             count+=1
#             if(count>K):
#                 break
#             docid=sorted_rd[i][0]
#             print(docid)
#             title=find_file_title(docid,toptitlecontents)
#             if title==None:
#                 count=count-1
#             else:
#                 print(title[:-1])
# else:
#     print("No matches\n")


# In[478]:


if __name__=="__main__":
    queries=[]
    out=open("queries_op.txt","w+")
    qtxt=sys.argv[1]
    print(qtxt)
    with open(qtxt ,"r") as q:
        queries=q.readlines()
#     print(len(queries))
    # global a
    # global categories
#     no_of_query=0

    for query in queries:
        start=time.time()
        query=query.rstrip('\n')
#         print(query)
        a=[]
        categories=[]
        process_query(query)
        query_words=a
        # print(a)
        # print(categories)
        rd=RankDox()
        if(rd!=-1):
            toptitlecontents=open(titledir+"top").readlines()
            sorted_rd=sorted(rd.items(),key=operator.itemgetter(1),reverse=True)
            if(len(sorted_rd)==0):
                out.write("No matches\n")
            else:
                count=0
                for i in range(len(sorted_rd)):
                    count+=1
                    if(count>K):
                        break
                    docid=sorted_rd[i][0]
#                     print(docid)

                    title=find_file_title(docid,toptitlecontents)
                    if title==None:
                        count=count-1
                    else:
#                         print(docid)
#                         print(title[:-1])
                        out.write(str(docid)+", "+title)
        else:
            out.write("No matches\n")
#         no_of_query+=1
        end=time.time()
        out.write(str(end-start)+", "+str((end-start)/K)+'\n\n')

#     end=datetime.now()
    out.close()



# In[ ]:
