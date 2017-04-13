from pprint import pprint
from Parser import Parser
import util
import os
import os.path
import tfidf

class VectorSpace:
    """ A algebraic model for representing text documents as vectors of identifiers. 
    A document is represented as a vector. Each dimension of the vector corresponds to a 
    separate term. If a term occurs in the document, then the value in the vector is non-zero.
    """

    #Collection of document term vectors
    documentVectors = [None] * 2047
    tfidfdocumentVectors = [None] * 2047

    tfidfvectorKeywordIndex =[]

    #Mapping of vector index to keyword
    vectorKeywordIndex=[]

    #Tidies terms
    parser=None
    documentID=[]
    tdidocuments = []
    tfidfcleandoclist = []

    def __init__(self, documents=[],documentsId=[]):
        self.documentVectors=[]
        self.parser = Parser()
        self.documentID = documentsId  
        self.tdidocuments= documents
        if(len(documents)>0):
            self.build(documents)
    def buildtfidfdocument(self,documents):
       
        self.tfidfvectorKeywordIndex = self.getVectorKeywordIndex(documents)
        self.tfidfcleandoclist = [self.cleanwords(document) for document in documents]
        
        
    def build(self,documents):
        """ Create the vector space for the passed document strings """
        self.vectorKeywordIndex = self.getVectorKeywordIndex(documents)
        self.documentVectors = [self.makeVector(document) for document in documents]

        #print self.vectorKeywordIndex
        #print self.documentVectors


    def getVectorKeywordIndex(self, documentList):
        """ create the keyword associated to the position of the elements within the document vectors """

        #Mapped documents into a single word string	
        vocabularyString = " ".join(documentList)

        vocabularyList = self.parser.tokenise(vocabularyString)
        #Remove common words which have no search value
        vocabularyList = self.parser.removeStopWords(vocabularyList)
        uniqueVocabularyList = util.removeDuplicates(vocabularyList)

        vectorIndex={}
        offset=0
        #Associate a position with the keywords which maps to the dimension on the vector used to represent this word
        for word in uniqueVocabularyList:
            vectorIndex[word]=offset
            offset+=1
        return vectorIndex  #(keyword:position)


    def makeVector(self, wordString):
        """ @pre: unique(vectorIndex) """

        #Initialise vector with 0's
        vector = [0] * len(self.vectorKeywordIndex)
        wordList = self.parser.tokenise(wordString)
        wordList = self.parser.removeStopWords(wordList)
        for word in wordList:
            vector[self.vectorKeywordIndex[word]] += 1; #Use simple Term Count Model
        return vector
    def tfidfmakeVector(self, wordString):
        """ @pre: unique(vectorIndex) """

        #Initialise vector with 0's
        vector = [0] * len(self.vectorKeywordIndex)
        wordList = self.parser.tokenise(wordString)
        wordList = self.parser.removeStopWords(wordList)
        for word in wordList:
            vector[self.vectorKeywordIndex[word]] = 1; #Use simple Term Count Model
        return vector
    def cleanwords(self, wordString):
        
        wordList = self.parser.tokenise(wordString)
        wordList = self.parser.removeStopWords(wordList)
        return wordList

    def buildQueryVector(self, termList):
        """ convert query string into a term vector """
        query = self.makeVector(" ".join(termList))
        return query


    def related(self,documentId):
        """ find documents that are related to the document indexed by passed Id within the document Vectors"""
        ratings = [util.cosine(self.documentVectors[documentId], documentVector) for documentVector in self.documentVectors]
        #ratings.sort(reverse=True)
        return ratings


    def search(self,searchList):
        """ search for documents that match based on a list of terms """
        queryVector = self.buildQueryVector(searchList)
        documentsID = self.documentID
        rating=[None]*2
        ratings=[]
        for i in range(len(documentsID)):
            ratings.append([util.cosine(queryVector, self.documentVectors[i]),documentsID[i]])
 #      ratings = [util.cosine(queryVector, documentVector) for documentVector in self.documentVectors]
        ratings.sort(reverse=True)
        return ratings[0:5]
    
    def searchJaccard(self,searchList):
        queryVector = self.buildQueryVector(searchList)
        documentsID = self.documentID
        rating=[None]*2
        ratings=[]
        for i in range(len(documentsID)):
            ratings.append([util.jaccard(queryVector, self.documentVectors[i],documentsID[i]),documentsID[i]])

 #      ratings = [util.cosine(queryVector, documentVector) for documentVector in self.documentVectors]
        ratings.sort(reverse=True)
        return ratings[0:5]
    def tfidfindex(self,dic):
        dictlist1= []
        dictlist2 =[]
        i=0
        for key, value in dic.iteritems():
         temp1 = key
         temp2 = value
         dictlist1.append(temp1)
         dictlist2.append(temp2)
        vector = [0] * len(self.vectorKeywordIndex)        
        for dic in dictlist1:
            vector[self.vectorKeywordIndex[dic]] = dictlist2[i]
            i=i+1           
        return vector
        
    def tfidfSearch(self, searchList):
        j=0
        self.buildtfidfdocument(self.tdidocuments)
        tbsearchList = self.cleanwords(searchList)
        tfidfsearchdic = {word: tfidf.tfidf(word, tbsearchList, self.tfidfcleandoclist) for word in tbsearchList}
        tfidfsearchlist = self.tfidfindex(tfidfsearchdic)
        documentsID = self.documentID
        rating=[None]*2
        ratings=[]
        for doc in self.tfidfcleandoclist:
           tfidfratings={word: tfidf.tfidf(word, doc, self.tfidfcleandoclist) for word in doc}
           tfidfratingslist = self.tfidfindex(tfidfratings)
           ratings.append([util.cosine(tfidfsearchlist,tfidfratingslist),documentsID[j]])
           j=j+1
        ratings.sort(reverse=True)
        return ratings[0:5]
        
documents = [None]*2047
documentsId = [None]*2047
i=0
for file in os.listdir("/Users/JohnLiu/CodeProject/codes/Documents"):
    if file.endswith(".product"):
        f = open(file, 'r')
        documents[i]=f.read()
        documentsId[i]=file
        f.close()
        i = i+1

        

if __name__ == '__main__':
    #test data
    print documents[5]

    vectorSpace = VectorSpace(documents,documentsId)

    #print vectorSpace.vectorKeywordIndex

    #print  vectorSpace.documentVectors

    #pprint(vectorSpace.related(1))
    print  "Q1"
    pprint(vectorSpace.search(["drill wood sharp"]))
    print  "Q2"
    pprint(vectorSpace.searchJaccard(["drill wood sharp"]))
    print  "Q3"
    pprint(vectorSpace.tfidfSearch("drill wood sharp"))
    print  "Q4"
    pprint(vectorSpace.searchJaccard(["drill wood sharp"]))
###################################################
