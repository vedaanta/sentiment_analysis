import re
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet_ic
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as po
from sklearn import svm
from nltk.stem.porter import PorterStemmer
from nltk import ngrams

st=PorterStemmer()
stop=[word.encode("utf-8") for word in stopwords.words("english")]

def dataFromFile(fname):
    file_iter = open(fname, 'rU')
    for line in file_iter:
        line = line.strip()                        
        record = (line.split('\t'))
        yield record

def dataFromFile1(fname):
    file_iter = open(fname, 'rU')
    for line in file_iter:
        line = line.strip()
        record = (line.split(','))
        yield record

def mapper(val):
    if(val=='positive'):
        return 2
    if(val=='neutral'):
        return 1
    return 0

def tagger(sentence):
    text = sentence.decode("utf-8").split()
    taggedText = nltk.pos_tag(text)
    return taggedText

def hashtag(string):
    listi= (re.findall(r"#[\w']+", string))
    listi=string.decode("utf-8").split()
    htags=[]
    count=[0,0,0]

    for i in range(len(listi)):
        if(len(list(swn.senti_synsets(listi[i])))>0):
            nscore=(list(swn.senti_synsets(listi[i]))[0]).neg_score()
            pscore=(list(swn.senti_synsets(listi[i]))[0]).pos_score()
            if(pscore==nscore):
                count[0]=count[0]+1
            if(pscore>nscore):
                count[1]=count[1]+1
            if(pscore<nscore):
                count[2]=count[2]+1


    return (count)

def userid(word):
    if word[0]=='@':
        return 1
    return 0

def findingResnikSimilarity(synset1, synset2):
    if wn.synset(synset1).path_similarity(wn.synset(synset2)) and wn.synset(synset2).path_similarity(wn.synset(synset1)):
        return (max (wn.synset(synset1).path_similarity(wn.synset(synset2)), wn.synset(synset2).path_similarity(wn.synset(synset1))))
    elif wn.synset(synset1).path_similarity(wn.synset(synset2)):
        return wn.synset(synset1).path_similarity(wn.synset(synset2))
    elif wn.synset(synset2).path_similarity(wn.synset(synset1)):
        return wn.synset(synset2).path_similarity(wn.synset(synset1))
    else:
        return 0

def swnScore(sentence):

    total=0;
    counter=0

    for sz in range(1,4):

        y=ngrams(word_tokenize(sentence.decode("utf-8")),sz)
        yy=['_'.join(grams) for grams in y]
        
        for z in yy:

            # if sz>1:
                # print sz,z 
            if(len(list(swn.senti_synsets(z)))>0 and z not in stop):
                if userid(z):
                    continue

                # if sz>1:
                #     print "!@#$"

                pos=(list(swn.senti_synsets(z))[0]).pos_score()
                neg=(list(swn.senti_synsets(z))[0]).neg_score()
                temp=1+pos-neg
                if temp==1:
                    continue
                counter+=1
                total+=temp

    if(counter==0):
        return 1
    return(total/counter)


def qmark(string):
    list= (re.findall(r"\?", string))
    for i in list:
        if i=='?':
            return 1
    return 0

def eclamark(string):
    list= (re.findall(r"!", string))
    for i in list:
        if i=='!':
            return 1
    return 0

def ohso(string ):
    list= (re.findall(r"(?i)Oh so [#\w]+", string))
    for i in list:
        return 1
    return 0

def  train():

    finp = dataFromFile('training_tweets1.txt')
    fout = open('trainingfeatures.txt','w')

    fout.write('swnval,pos,neg,neut,yval'+'\n')
    k=0
    print ("Training in progress ....")
    for i in finp:

        yval=mapper(i[0])
        swnval=swnScore(i[1])

        hashval=hashtag(i[1])
        pos=hashval[1]
        neg=hashval[2]
        neut=hashval[0]
        k+=1
        fout.write(str(swnval)+','+str(pos)+','+str(neg)+','+str(neut)+','+str(yval)+'\n')
        print (k)
    print ("Training Completed")

def test():

    finp= dataFromFile('test_tweets1.txt')
    fout= open('testfeatures.txt','w')

    k=0
    for i in finp:

        yval=mapper(i[0])
        swnval=swnScore(i[1])
        hashval=hashtag(i[1])
        pos=hashval[1]
        neg=hashval[2]
        neut=hashval[0]
        k+=1
        fout.write(str(swnval)+'\t'+str(pos)+'\t'+str(neg)+'\t'+str(neut)+'\t'+str(yval)+'\t'+i[1]+'\t'+i[0]+'\n')
        print(k)

def classify():

    x = po.read_csv('trainingfeatures.txt')
    a=x['swnval']
    b=x['pos']
    c=x['neg']
    d=x['neut']
    Y=x['yval']

    data =po.concat([a,b,c,d],axis=1)
    print("Training of model in progress ....")
    clf = svm.SVC(kernel='rbf',C=1,max_iter=-1,tol=0.00001)
    clf.fit(data,Y)
    print('Model is trained')
    finp=dataFromFile('testfeatures.txt')
    ans=0
    qq=0

    for i in finp:
        k=i[0:4]
        temp=clf.predict([k])
        # print int(temp[0]), int(i[4])
        if(int(temp[0])==int(i[4])):
            ans+=1
            print ans
        qq+=1

    acc=1.0*ans/qq
    acc=acc*100
    
    print acc

train()
test()
classify()