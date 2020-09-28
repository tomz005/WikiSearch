#!/usr/bin/env python
# coding: utf-8

# In[8]:


import xml.sax
import nltk
import re
import os
import sys
from nltk.corpus import stopwords
from datetime import datetime
import Stemmer
import unicodedata
import time

indexcount=0
fc=0
raw_token_count=0
processed_token_count=0
docTitle={}
# indexFile = open("../Index/MyTitle","w")
stemmer=Stemmer.Stemmer('english')
# stopWords = stopwords.words('english')
# stopWordsdict=defaultdict(int)
# additionalwords=["ref","/ref","references","reflist"]
# for word in additionalwords:
#     stopWords.append(word)
# for word in stopWords:
#     stopWordsdict[word]=1


# In[9]:


class WikiDumpHandler(xml.sax.handler.ContentHandler):

    def __init__(self):
        self.tag = ""
        self.documentID = ""
        self.regex = re.compile(r'[a-zA-Z]+')
        self.docMap = {}
#         self.docTitle = {}
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
        global docTitle
#         data=unicodedata.normalize('NFKD',data).encode('ASCII','ignore')
        data.encode('ascii', 'ignore')
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
            docTitle[str(int(self.documentID))]=self.title
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
#             for did in sorted(self.docTitle,key=int):
#                 indexFile.write(did+" "+("").join(self.docTitle[did])+"\n")
#             global indexcount+=len(self.dic.keys())
#             print(indexcount)
#             print("titlemapping done\n")
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
        global fc
        fc = fc+1
        f="../Index/idx"+str(fc)+".txt"
#         f="../Index/invertindex.txt"
        op=open(f,"w+")
        word=""
        for x in sorted(self.dic):
#             print(x)
#             print("\n")
            word=x+" "
            for g in self.dic[x]:
                word +=str(int(g))
                word+=self.get_val("t",self.dic[x][g][0])
                word+=self.get_val("x",self.dic[x][g][1])
                word+=self.get_val("i",self.dic[x][g][2])
                word+=self.get_val("c",self.dic[x][g][3])
                word+=self.get_val("l",self.dic[x][g][4])
                word+=self.get_val("r",self.dic[x][g][5])
                word+="|"
            word=word[:-1]
            op.write(word+"\n")
#             self.dic={}
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








# In[10]:


# # print(os.listdir("../DATASET/Phase2/"))
# files = os.listdir('../DATASET/Phase2/')
# print(len(files))


# In[11]:


count = 1
indextop = []
indextop2 = []
listoflines = []
path = '../Split/'
pathtitle = '../Title/'
counterl = 0
counter = 1
end = len(os.listdir("../Index/")) + 1


# In[12]:


def merge_files(inp1,inp2,out):
    print(inp1)
    print(inp2)
    print(out)
    with open(inp1,"r+") as f1,open(inp2,"r+") as f2:
        with open(out,"w+") as o:
            line1=f1.readline()
            line2=f2.readline()
            content1=line1.split()
            content2=line2.split()
            while(line1!='' and line2!=''):
                if(content1[0]<content2[0]):
                    o.write(line1)
                    line1=f1.readline()
                    content1=line1.split()
                elif(content1[0]>content2[0]):
                    o.write(line2)
                    line2=f2.readline()
                    content2=line2.split()
                else:
                    line=content1[0]+" "+content1[1]+"|"+content2[1]
                    o.write(line+'\n')
                    line1=f1.readline()
                    content1=line1.split()
                    line2=f2.readline()
                    content2=line2.split()
            while(line1!=''):
                o.write(line1)
                line1=f1.readline()
            while(line2!=''):
                o.write(line2)
                line2=f2.readline()




# In[13]:


def merging():
    global counter
    global end
    while counter<end-1:
        if counter==end-2:
            merge_files("../Index/idx"+str(counter)+".txt","../Index/idx"+str(counter+1)+".txt","../Index/MyIndex")
        else:
            merge_files("../Index/idx"+str(counter)+".txt","../Index/idx"+str(counter+1)+".txt","../Index/idx"+str(end)+".txt")
        print("Merging done"+str(counter)+" & "+str(counter+1))
        print(end)
        counter+=2


# In[14]:


def getblockIndex(indexpath):
    global count
    global listoflines
    global indextop
    with open(indexpath) as indexfile:
        for line in indexfile:
            if(count%10000==0):
                counter=str(count/10000)
                indextop.append(indexfilewrite(counter,listoflines))
                listoflines=[]
            listoflines.append(line)
            count+=1
        if(len(listoflines)!=0):
            counter=str((count+10000)/10000)
            indextop.append(indexfilewrite(counter,listoflines))
            listoflines=[]

def getblockTitle(titlepath):
    global count
    global listoflines
    global indextop
    with open(titlepath) as titlefile:
        for line in titlefile:
            if(count%500==0):
                counter=str(count/500)
                indextop.append(titlefilewrite(counter,listoflines))
                listoflines=[]
            listoflines.append(line)
            count+=1
        if(len(listoflines)!=0):
            counter=str((count+500)/500)
            indextop.append(titlefilewrite(counter,listoflines))
            listoflines=[]



# In[15]:


def makelayersIndex():
    global indextop
    global indextop2
    global count
    while(len(indextop)>50):
        indextop2=[]
        indexlist=[]
        count=1
        for idx in indextop:
            if(count%50==0):
                counter=str(count/50)
                indextop2.append(indexfilewritel(counter,indexlist))
                indexlist=[]
            indexlist.append(idx)
            count+=1
        if(len(indexlist)!=0):
            counter=str((count+50)/50)
            indextop2.append(indexfilewritel(counter,indexlist))
            indexlist=[]
        global counterl
        counterl+=1
        indextop=indextop2

def makelayersTitle():
    global indextop
    global indextop2
    global count
    if(len(indextop)<=200):
        indextop2=indextop
    while(len(indextop)>200):
        indextop2=[]
        indexlist=[]
        count=1
        for idx in indextop:
            if(count%200==0):
                counter=str(count/200)
                indextop2.append(titlefilewritel(counter,indexlist))
                indexlist=[]
            indexlist.append(idx)
            count+=1
        if(len(indexlist)!=0):
            counter=str((count+200)/200)
            indextop2.append(titlefilewritel(counter,indexlist))
            indexlist=[]
        global counterl
        counterl+=1
        indextop=indextop2


# In[16]:


def makefirstIndex():
    global indextop2
    filepath=path+'top'
    ff=open(filepath,"w")
    for line in indextop2:
        ff.write(line)
    ff.close()

def makefirstTitle():
    global indextop2
    filepath=pathtitle+'top'
    ff=open(filepath,"w")
    for line in indextop2:
        ff.write(line)
    ff.close()


# In[21]:


def indexfilewrite(counter,listoflines):
    out=path+counter
#     print(out)
    of=open(out,"w")
    firstline=listoflines[0][:-1].split(" ")[0]+" "+counter+" NL\n"
    for line in listoflines:
        of.write(line)
    of.close()
    return firstline

def titlefilewrite(counter,listoflines):
    out=pathtitle+counter
    of=open(out,"w")
    firstline=listoflines[0][:-1].split(" ")[0]+" "+counter+" NL\n"
    for line in listoflines:
        of.write(line)
    of.close()
    return firstline


# In[22]:


def indexfilewritel(counter,listoflines):
    global counterl
    out=path+"L"+str(counterl)+counter
#     print(out)
#     print(str(counterl))
#     print(counter)
    of=open(out,"w")
    firstline=listoflines[0][:-1].split(" ")[0]+" "+"L"+str(counterl)+counter+" NL\n"
    for line in listoflines:
        of.write(line)
    of.close()
    return firstline

def titlefilewritel(counter,listoflines):
    global counterl
    out=pathtitle+"L"+str(counterl)+counter
    of=open(out,"w")
    firstline=listoflines[0][:-1].split(" ")[0]+" "+"L"+str(counterl)+counter+" NL\n"
    for line in listoflines:
        of.write(line)
    of.close()
    return firstline


# In[19]:


def createindexblock():
    getblockIndex("../Index/MyIndex")
#     getlastIndex()
    makelayersIndex()
    makefirstIndex()

def createtitleblock():
    getblockTitle("../Index/MyTitle")
#     getlastTitle()
    makelayersTitle()
    makefirstTitle()


# In[23]:


def reinit():
    global count
    global indextop
    global indextop2
    global listoflines
    global counterl
    count = 1
    indextop = []
    indextop2 = []
    listoflines = []
    counterl = 0


# In[24]:


if __name__=="__main__":
    '''
    global docTitle
    handler=WikiDumpHandler()
    parser=xml.sax.make_parser()
    parser.setContentHandler(handler)
#     dumppath=sys.argv[1]
#     indexpath=sys.argv[2]
#     statpath=sys.argv[3]
#     print(dumppath)
#     print(indexpath)
#     print(statpath)
#     os.mkdir(indexpath)
#     f="../Index/"
    indexFile = open("../Index/MyTitle","w")
#     indexFile=open(statpath)
#     startTime = datetime.now()
#     parser.parse('../DATASET/enwiki-20200801-pages-articles-multistream1.xml-p1p30303')

#     print(datetime.now() - startTime)

    files=os.listdir("../DATASET/Phase2/")
#     files=['../DATASET/enwiki-20200801-pages-articles-multistream1.xml-p1p30303']
    for file in files:
        print("Started parsing : "+file)
        startTime = datetime.now()
        parser.parse('../DATASET/Phase2/'+file)
        print("Parsing ended for : "+file)
        print(datetime.now() - startTime)
        time.sleep(5)
    for did in sorted(docTitle,key=int):
        indexFile.write(did+" "+("").join(docTitle[did])+"\n")
    indexFile.close()
    print(raw_token_count)
    print("\n")
    print(processed_token_count)
    '''
#     if not os.path.exists('../Split'):
#         os.mkdir('../Split')
#     if not os.path.exists('../Title'):
#         os.mkdir('../Title')
    createindexblock()
    reinit()
    createtitleblock()


# In[ ]:





# In[ ]:
