import sys
import operator
from pprint import pprint
#http://www.scipy.org/
try:
	from numpy import dot
	from numpy.linalg import norm
	
except:
	print ("Error: Requires numpy from http://www.scipy.org/. Have you installed scipy?")
	sys.exit() 

def removeDuplicates(list):
	""" remove duplicates from a list """
	return set((item for item in list))


def cosine(vector1, vector2):
	""" related documents j and q are in the concept space by comparing the vectors :
		cosine  = ( V1 * V2 ) / ||V1|| x ||V2|| """
	return float(dot(vector1,vector2) / (norm(vector1) * norm(vector2)))
def tfidfcosine(tfidf1,tfidf2):
    dictlist1 =[]
    dictlist2 =[]
    for key, value in tfidf1.iteritems():
      temp = [value]
      dictlist1.append(temp)
    for key, value in tfidf2.iteritems():
      temp = [value]
      dictlist2.append(temp)
    return cosine(dictlist1, dictlist2)


def jaccard(vector1, vector2,did):
        vectorSum = []
        for i in range(len(vector1)):
         if vector2[i]>=2:
            vector2[i]=1
         vectorSum.append(vector1[i]+vector2[i])
        vectorResult = float(vectorSum.count(2))/(vectorSum.count(1)+vectorSum.count(2))
        return vectorResult 
