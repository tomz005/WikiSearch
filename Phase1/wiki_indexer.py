#!/usr/bin/env python
# coding: utf-8

# In[33]:


# import xml.sax


# In[34]:


# class WikiXmlHandler(xml.sax.handler.ContentHandler):
#     def __init__(self):
#         xml.sax.handler.ContentHandler.__init__(self)
#         self._buffer = None
#         self._values = {}
#         self._current_tag = None
#         self._pages = []

#     def characters(self, content):
#         """Characters between opening and closing tags"""
#         if self._current_tag:
#             self._buffer.append(content)

#     def startElement(self, name, attrs):
#         """Opening tag of element"""
#         if name in ('title', 'text'):
#             self._current_tag = name
#             self._buffer = []

#     def endElement(self, name):
#         """Closing tag of element"""
#         if name == self._current_tag:
#             self._values[name] = ' '.join(self._buffer)

#         if name == 'page':
#             self._pages.append((self._values['title'], self._values['text']))


# In[35]:


# handler=WikiXmlHandler()
# parser=xml.sax.make_parser()
# parser.setContentHandler(handler)
# parser.parse('../DATASET/enwiki-20200801-pages-articles-multistream1.xml-p1p30303')


# In[1]:


# handler._pages


# In[9]:


# len(handler._pages)


# In[70]:


# for i in range(0,len(handler._pages)):
#     if(handler._pages[i][0]=='Lafora disease'):
#         print(i)


# In[1]:


import xml.sax
import nltk
import re
import os
import sys
from nltk.corpus import stopwords
from datetime import datetime
import Stemmer

# indexcount=0
# raw_token_count=0
# processed_token_count=0
# indexFile = open("../Index/MyTitle","w")
stemmer=Stemmer.Stemmer('english')
# stopWords = stopwords.words('english')
# stopWordsdict=defaultdict(int)
# additionalwords=["ref","/ref","references","reflist"]
# for word in additionalwords:
#     stopWords.append(word)
# for word in stopWords:
#     stopWordsdict[word]=1


# In[2]:


class WikiDumpHandler(xml.sax.handler.ContentHandler):

    def __init__(self):
        self.tag = ""
        self.documentID = ""
        self.regex = re.compile(r'[a-zA-Z]+')
        self.docMap = {}
        self.docTitle = {}
        self.dic = {}
        self.stopWords = {}
        self.getStopWords()
        self.temp = 0
        self.pageTag=0

    def startElement(self,name,attributes):
        self.tag=name
        if(self.tag=='page'):
            self.title=[]
            self.body=[]
            self.infobox=[]
            self.category=[]
            self.reference=[]
            self.link=[]
            self.pageTag=0
            self.infoboxTag=0
            self.referenceTag=0
            self.categoryTag=0
            self.linkTag=0
        if(self.tag =='title'):
            self.pageTag=1

#     def endElement(self,tag):
#         self.tag=tag
#         if(self.tag=='page'):
#             print("end of page\n")

    def characters(self,data):
#         data=unicode.normalize('NFKD',data).encode('ASCII','ignore')
        data=data.strip()
#         print(data)
#         print('\n')
        if(self.tag=='page'):
            if(self.referenceTag!=0):
                if(len(data)==0):
                    self.referenceTag=0
                    return
            if(self.linkTag!=0):
                if(len(data)==0):
                    self.linkTag=0
                    return

        if(len(data)==0):
            return
        if(self.tag=='title'):
            self.title.append(data.lower())
        elif(self.tag=='id' and self.pageTag==1):
            self.documentID=data
            self.docTitle[str(int(self.documentID))]=self.title
            self.pageTag=0
        elif(self.tag=='text'):
            self.infoboxTag=self.checkinfobox(data)
            self.linkTag=self.checklink(data)
            self.referenceTag=self.checkreference(data)
            self.categoryTag=self.checkcategory(data)
#             print(self.title)
#             print("\n")
#             print(self.infoboxTag)
#             print("\n")
            if(self.categoryTag==1):
                self.category.append(data[11:-2].lower())
            elif(self.infoboxTag==1):
                if(data.find("{{InfoBox")!=-1):
                    self.infobox.append(data[9:].lower())
                else:
                    self.infobox.append(data.lower())
            elif(self.linkTag==1):
                if(data.find("==External links==")==-1):
                    if(data[0]=='*'):
                        self.link.append(data.lower())
            elif(self.referenceTag==1):
                if(data.find("==References==")==-1):
                    self.reference.append(data.lower())
            else:
                self.body.append(data.lower())

    def get_val(self,field,count):
        if(int(count)==0):
            return ""
        else:
            return field+str(count)

    def endElement(self,name):
        self.tag=name
#         print("------------------------------------\n")
#         print("T : \n")
#         print(self.title)
#         print("I : "+self.category+"\n")
        if(self.tag=='page'):
# #             print(self.title)
# #             print(self.link)
#             if(len(self.reference)!=0):
#                 print(self.title)
#                 print(self.reference)
            self.createIndex(self.title,0)
            self.createIndex(self.body,1)
            self.createIndex(self.infobox,2)
            self.createIndex(self.category,3)
            self.createIndex(self.link,4)
            self.createIndex(self.reference,5)
#             if(sys.getsizeof(self.dic)>1000000):
#                 global indexcount
#                 indexcount+=len(self.dic.keys())
#                 self.filewrite()
#                 self.dic={}
        elif(self.tag=='mediawiki'):
            for did in sorted(self.docTitle,key=int):
                indexFile.write(did+" "+("").join(self.docTitle[did])+"\n")
#             global indexcount+=len(self.dic.keys())
#             print(indexcount)
            # print("titlemapping done\n")
            self.filewrite()
            self.dic={}

    def checkcategory(self,data):
        if(data.find("[[Category:")!=-1):
            return 1
        else:
            return 0

    def checkinfobox(self,data):
        if(self.infoboxTag == 0):
            if(data.find("{{Infobox") != -1):
                return 1
            else:
                return 0
        else:
            if(data == "}}"):
                return 0
            else:
                return 1

    def checklink(self,data):
        if(self.linkTag==0):
            if(data.find("==External links==")!=-1):
                return 1
            else:
                return 0
        else:
            if(data.startswith("==")):
                return 0
            else:
                return 1

    def checkreference(self,data):
        if(self.referenceTag==0):
            if(data.find("==References==")!=-1):
                return 1
            else:
                return 0
        else:
            return 1

    def filewrite(self):
#         global fc
#         fc = fc+1
#         f=filename+str(fc)+".txt"
#         f="../Index/invertindex.txt"
        op=open(f,"w")
        word=""
        for x in sorted(self.dic):
#             print(x)
#             print("\n")
            word=x+" "
            for g in self.dic[x]:
                word +=str(int(g))
                word+=self.get_val("t",self.dic[x][g][0])
                word+=self.get_val("b",self.dic[x][g][1])
                word+=self.get_val("i",self.dic[x][g][2])
                word+=self.get_val("c",self.dic[x][g][3])
                word+=self.get_val("l",self.dic[x][g][4])
                word+=self.get_val("r",self.dic[x][g][5])
                word+="|"
            word=word[:-1]
            op.write(word+"\n")
        op.close()

    def getStopWords(self):
        stopWords=stopwords.words('english')
        additionalwords=["ref","/ref","references","reflist"]
        for word in additionalwords:
            stopWords.append(word)
        for word in stopWords:
            self.stopWords[word]=1


#     def swremove(self,data):
#         return [w for w in data if stopWordsdict[w] != 1]

    def createIndex(self,data,index):
        for component in data:
            tokens=self.tokenize(component)
#             tokens=self.swremove(component)
            tokensList=[]
            for token in tokens:
                global raw_token_count
                raw_token_count+=1
                try:
                    self.stopWords[token]
                except:
                    final_token=token.strip('~`!@#$%^&*()_+=-\\|\"\';:/?.,')
                    if(len(final_token)>0):
                        if "-" in final_token:
                            if bool(re.match('^[0-9]{1,4}-([0-9]{1,4})-([0-9]{1,4})$',final_token)):
                                tokensList.append(final_token)
                        else:
                            tokensList.append(final_token)

            for word in tokensList:
                #Stemming is pending
                root=stemmer.stemWord(word)
                try:
                    self.dic[root][self.documentID]
                    self.dic[root][self.documentID][index]+=1

                except:
                    try:
                        self.dic[root]
                        self.dic[root][self.documentID]=[0,0,0,0,0,0]
                        self.dic[root][self.documentID][index]=1

                    except:
                        global processed_token_count
                        processed_token_count+=1
                        self.dic[root]={}
                        self.dic[root][self.documentID]=[0,0,0,0,0,0]
                        self.dic[root][self.documentID][index]=1

    def tokenize(self,sentence):
        regWhiteSpace = re.compile(u"[\s\u0020\u00a0\u1680\u180e\u202f\u205f\u3000\u2000-\u200a]+")
        sentence=regWhiteSpace.sub(" ",sentence).strip()
        sentence=re.sub('[:|\\|/|=|?|!|~|`|!|@|#|$|%|^|&|*|(||)|_+.\\|-|{|}|\[|\]|;|\"|\'|<|>|,|]',' ',sentence)
        sentence=re.sub(r'-(-+)|/(/+)',' ',sentence)
        sentence=re.sub(' \S ',' ',sentence)
#         sentence=re.sub(r'http[^\ ]*\ ',' ',sentence)
#         sentence=re.sub(r'&nbsp;|&lt;|&gt;|&amp;|&quot;|&apos;',' ',sentence)
        sentence=sentence.split()
        return sentence








# In[3]:


if __name__=="__main__":
    handler=WikiDumpHandler()
    parser=xml.sax.make_parser()
    parser.setContentHandler(handler)
    raw_token_count=0
    processed_token_count=0
    dumppath=sys.argv[1]
    indexpath=sys.argv[2]
    statpath=sys.argv[3]
    # print(dumppath)
    # print(indexpath)
    # print(statpath)
    if not os.path.exists(indexpath):
        os.mkdir(indexpath)
    f=indexpath+"index.txt"
    indexFile = open(indexpath+"MyTitle","w")
#     indexFile=open(statpath)
    startTime = datetime.now()
    parser.parse(dumppath)
    print(datetime.now() - startTime)
    indexFile.close()
    statFile=open(statpath,"w")
    statFile.write(str(raw_token_count)+"\n")
    statFile.write(str(processed_token_count))
    statFile.close()
    # print(raw_token_count)
    # print("\n")
    # print(processed_token_count)


# In[ ]:
