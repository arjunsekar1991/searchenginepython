
'''
query processing

'''
from cranqry import loadCranQry
from index import InvertedIndex
from cran import CranFile
import re
import numpy as np
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from functools import reduce
from collections import Counter
from norvig_spell import correction
import math
import decimal
import sys
class QueryProcessor:

    def __init__(self, query, index, collection, numofresults):
        ''' index is the inverted index; collection is the document collection'''
        self.raw_query = query
        self.index = index
        self.docs = collection
        self.preprocessed_query_tokens = {}
        self.intermediateResultVectorQuery = {}
        self.queryId = 0
        self.numofresults = numofresults

    def preprocessing(self):
        ''' apply the same preprocessing steps used by indexing,
            also use the provided spelling corrector. Note that
            spelling corrector should be applied before stopword
            removal and stemming (why?)'''

        #ToDo: return a list of terms


        for q in self.raw_query:
            query_tokens = []
            stemmed_query_tokens = []
#            print(q, self.raw_query[q].text)
         #   query_tokens = re.split(" ", self.raw_query[q].text.replace('\n', ' '))
            query_tokens = word_tokenize(self.raw_query[q].text)
            query_tokens = [element.lower() for element in query_tokens];
            tempcounter = 0
            while tempcounter < len(query_tokens):
                query_tokens[tempcounter] = correction(query_tokens[tempcounter]);
                tempcounter = tempcounter + 1
            ps = PorterStemmer()
            temp = 0
            querytokentemp = 0
            while temp < len(query_tokens):

                query_tokens[temp] = ps.stem(query_tokens[temp])
                querytokentemp = querytokentemp + 1
                with open("stopwords") as f:
                    for line in f:
                        if line.strip() == query_tokens[temp]:
                            query_tokens.remove(line.strip())
                            temp = temp - 1
                temp = temp + 1
            self.preprocessed_query_tokens[q] = query_tokens


    def booleanQuery(self):
        ''' boolean query processing; note that a query like "A B C" is transformed to "A AND B AND C" for retrieving posting lists and merge them'''
        #ToDo: return a list of docIDs

        for q in self.preprocessed_query_tokens:
            if q == self.queryId:
                resultsDocIds = []
#                print(q)# this prints query id
                templist = self.preprocessed_query_tokens.get(q)
    #            print(templist)
                i = 0
                while i < len(templist):
    #                print("query token --> " + templist[i])
                    if templist[i] in self.index.items:
    #                        print(list(self.index.items.get(templist[i]).get('posting').keys()))
                            resultsDocIds.append(list(self.index.items.get(templist[i]).get('posting').keys()))
                    else:
                            resultsDocIds.append(list([0]))
                    i = i + 1
                print(reduce(np.intersect1d, resultsDocIds))


    def vectorQuery(self, k):
        ''' vector query processing, using the cosine similarity. '''
        #ToDo: return top k pairs of (docID, similarity), ranked by their cosine similarity with the query in the descending order
        # You can use term frequency or TFIDF to construct the vectors
        #constructing document vector for document 1
        vectorResult = []
        cf = CranFile('cran.all')
        documentVector = {}
        queryVector = {}
        ps = PorterStemmer()
        finalResult = {}
        for q in self.raw_query:
            if q == self.queryId:
                query_tokens = []
                stemmed_query_tokens = []
                #            print(q, self.raw_query[q].text)
                #   query_tokens = re.split(" ", self.raw_query[q].text.replace('\n', ' '))
                query_tokens = word_tokenize(self.raw_query[q].text)
                query_tokens = [element.lower() for element in query_tokens];
                tempcounter = 0
                while tempcounter < len(query_tokens):
                    query_tokens[tempcounter] = correction(query_tokens[tempcounter]);
                    tempcounter = tempcounter + 1
                ps = PorterStemmer()
                temp = 0
                querytokentemp = 0
                while temp < len(query_tokens):

                    query_tokens[temp] = ps.stem(query_tokens[temp])
                    querytokentemp = querytokentemp + 1
                    with open("stopwords") as f:
                        for line in f:
                            if line.strip() == query_tokens[temp]:
                                query_tokens.remove(line.strip())
                                temp = temp - 1
                    temp = temp + 1

                #block to calculate query vector start

                temp2 = 0
                while temp2 < len(query_tokens):
                    if query_tokens[temp2] in self.index.items:
                        wordfreq = [query_tokens.count(query_tokens[temp2])]
       #                 print(wordfreq)
                        queryVector[query_tokens[temp2]] = (self.index.items[query_tokens[temp2]].get('idf') )* (1 + math.log( wordfreq[0] , 10))
                        temp2 = temp2 + 1
                    else:
                        queryVector[query_tokens[temp2]] = 0;
                        temp2 = temp2 + 1
                #block to calculate query vector end
                docidScorepair = {}
                for doc in cf.docs:
    #                print(doc.docID, doc.title, doc.body)

    #                print("generating document vector here")
                    titletoken = word_tokenize(doc.title)
                    bodytoken = word_tokenize(doc.body)
                    tokens = titletoken + bodytoken
                    tokens = [element.lower() for element in tokens];
                    temp3 = 0
                    while temp3 < len(tokens):
                        with open("stopwords") as f:
                            for line in f:
                                if line.strip() == tokens[temp3]:
                                    tokens.remove(line.strip())
                                    temp3 = temp3 - 1
                        temp3 = temp3 + 1
                    temp = 0
                    while temp < len(tokens):
                        tokens[temp] = ps.stem(tokens[temp])
                        temp = temp + 1
                    temp2 = 0
                    while temp2 < len(tokens):
                        if tokens[temp2] in self.index.items:
                            documentVector[tokens[temp2]] = (1 + math.log(self.index.items[tokens[temp2]].get('posting').get(doc.docID).get('termfreq'),10)) * (self.index.items[tokens[temp2]].get('idf'))
                            temp2 = temp2 + 1
                        else:
                            documentVector[tokens[temp2]] = 0;
                            temp2 = temp2 + 1
    #                print('document vector complete')
                    #print(documentVector)
                    # without normalization

                    #normalize query vector and document vector start
                    normalizequeryvectorcounter = 0
                    queryVectornormalized = []
#                    sumofsquaresquery = 0
#                    for z in queryVector:
#                        sumofsquaresquery =  sumofsquaresquery + np.multiply(queryVector[z] , queryVector[z])
#
#                    sumofsquaresquery = 1 / math.sqrt(sumofsquaresquery)


#                    for r in queryVector:
#                        queryVector[r] = queryVector[r] *  sumofsquaresquery

                    sumofsquaresdocument = 0
                    for l in documentVector:
                        sumofsquaresdocument = sumofsquaresdocument + np.multiply(documentVector[l], documentVector[l])
                    try:
                        sumofsquaresdocument = 1 / math.sqrt(sumofsquaresdocument)

                    except:
                        sumofsquaresdocument = 0
                    for h in documentVector:
                        documentVector[h] = documentVector[h] * sumofsquaresdocument
                    #noramlize ends

                    cosineVector = queryVector.copy()
                    for u in queryVector:
                        if u in documentVector:
                            cosineVector[u] = np.multiply(documentVector[u], queryVector[u])
                        else:
                            #below line is wrong
#                            cosineVector[k] = queryVector[k]
                            cosineVector[u] = 0
#                    print ("query vector -->")
#                    print(queryVector)
#                    print ("document vector -->")
#                    print( documentVector)
#                    print ("cosine vector -->")
#                    print(cosineVector)
#                    print ("****************************")
                    # document score

                    docidScorepair[doc.docID] = sum(cosineVector.values())
                    #end of document score

                    self.intermediateResultVectorQuery[q] = docidScorepair

                    cosineVector = {}
                    #end without normalization

                    documentVector = {}
                queryVector = {}

#                print(query_tokens)
                counterObject = Counter(self.intermediateResultVectorQuery[q])
                high = counterObject.most_common(k)
#                print('*** query id ***'+q + "***** query text *****" +self.raw_query[q].text)
                if k == 3:
                    print(high)
                vectorResult = [i[0] for i in counterObject.most_common(k)]
                #                print(vectorResult)
        return vectorResult


def test():
    ''' test your code thoroughly. put the testing cases here'''
    print('Pass')

def query( indexfilename,processingalgorithm,queryfilename, queryid, numresults=3):
    ''' the main query processing program, using QueryProcessor'''

    # ToDo: the commandline usage: "echo query_string | python query.py index_file processing_algorithm"
    # processing_algorithm: 0 for booleanQuery and 1 for vectorQuery
    # for booleanQuery, the program will print the total number of documents and the list of docuement IDs
    # for vectorQuery, the program will output the top 3 most similar documents

    qrys = loadCranQry(queryfilename)
#    for q in qrys:
#        print(q, qrys[q].text)

    loadiindex = InvertedIndex()
    loadiindex = loadiindex.load(indexfilename)
#    print("index loaded")

    cf = CranFile('cran.all')

    queryProcessor = QueryProcessor(qrys, loadiindex, cf.docs, numresults)
    if processingalgorithm == '0' :
        queryProcessor.preprocessing()
        queryProcessor.queryId = queryid
        results = queryProcessor.booleanQuery()
    if processingalgorithm == '1':
        queryProcessor.queryId = queryid
        results = queryProcessor.vectorQuery(queryProcessor.numofresults)
    return results
if __name__ == '__main__':
    #test()

    query(str(sys.argv[1]), str(sys.argv[2]),str(sys.argv[3]),str(sys.argv[4]))
