import re
import nltk
from nltk.classify import *

class ClassifierHelper:
    #start __init__
    def __init__(self, featureListFile):
        self.wordFeatures = []
        # Read feature list
        inpfile = open(featureListFile, 'r')
        line = inpfile.readline()        
        while line:
            self.wordFeatures.append(line.strip())
            line = inpfile.readline()
    #end    
    def is_ascii(self,s):
        return "".join(i for i in s if ord(i)<128)

    def removeNonAscii(s):
        return "".join(i for i in s if ord(i)<128)

    #start getStopWordList
    def getStopWordList(stopWordListFileName):
        #read the stopwords file and build a list
        stopWords = []
        stopWords.append('AT_USER')
        stopWords.append('URL')

        fp = open(stopWordListFileName, 'r')
        line = fp.readline()
        while line:
            word = line.strip()
            stopWords.append(word)
            line = fp.readline()
        fp.close()
        return stopWords
    #end

    #start getfeatureVector
    def getFeatureVector(self,tweet):
        f1=f2=f3=0
        featureVector = []
        #split tweet into words
        words = tweet.split()
        for w in words:
            #replace two or more with two occurrences
            w = self.replaceTwoOrMore(w)
            #strip punctuation
            w = w.replace('"','')
            w = w.replace('?','')
            w = w.replace('!','')
            w = w.replace('.','')
            #print w
            w= self.is_ascii(w)
            #print w
            #check if the word stats with an alphabet
            val = re.search(r"^[a-zA-Z][a-zA-Z0-9',\](>:#;=*+\[|\-/\\@<~^%$})]*$", w)
            #check if the word is an emoji
            val1 = re.search(r"^[(>:#;=*\[8|\-B/\\@<~^%$LXoO0}3Vb][a-zA-Z0-9',\](>:#;=*+\[|\-/\\@<~^%$})]*$",w)
            #ignore if it is a stop word
            if(w not in self.stopWords):
                for m in featureVector:
                    if w==m:
                        f1=1
                        break
                if(f1==0):
                    featureVector.append(w.lower())
                
            if (val is not None):
                for m in featureVector:
                    if w==m:
                        f2=1
                        break
                if(f2==0):
                    featureVector.append(w.lower())
                
            if(val1 is not None):
                pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
                emoticon=pattern.sub(r"\1", w)
                for m in featureVector:
                    if emoticon==m:
                        f3=1
                        break
                if f3==0:
                    featureVector.append(emoticon.lower())
                #print featureVector
        return featureVector
    #end
    stopWords = getStopWordList('stopwords1.txt')

    
    #start extract_features
    def extract_features(self,tweet):
        tweet_words = set(tweet)
        features = {}
        for word in self.wordFeatures:
            features['contains(%s)' % word] = (word in tweet_words)
        return features
    #end

    #start replaceTwoOrMore
    def replaceTwoOrMore(self, s):
        # pattern to look for three or more repetitions of any character, including
        # newlines.
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
        return pattern.sub(r"\1\1", s)
    #end
    
    #start process_tweet
    def processTweet(self,tweet):
        # process the tweets

        #Convert to lower case
        tweet = tweet.lower()
        #Convert www.* or https?://* to URL
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
        #Convert @username to AT_USER
        tweet = re.sub('@[^\s]+','AT_USER',tweet)
        #Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        #Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        #trim
        tweet = tweet.replace('"',"")
        #tweet=  tweet.strip()
        #tweet = tweet.rstrip('"')
        #tweet = tweet.lstrip('"')
        tweet = self.is_ascii(tweet)
        return tweet
    #end 
    
    #start is_ascii
    #end
#end class
