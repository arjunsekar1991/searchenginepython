
'''
query processing

'''
from cranqry import loadCranQry
from index import InvertedIndex
from cran import CranFile
import re
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from functools import reduce
class QueryProcessor:

    def __init__(self, query, index, collection):
        ''' index is the inverted index; collection is the document collection'''
        self.raw_query = query
        self.index = index
        self.docs = collection
        self.preprocessed_query_tokens = {}

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
            resultsDocIds = []
            print(q)# this prints query id
            templist = self.preprocessed_query_tokens.get(q)
#            print(templist)
            i = 0
            while i < len(templist):
#                print("query token --> " + templist[i])
                if templist[i] in self.index.items:
#                        print(list(self.index.items.get(templist[i]).get('posting').keys()))
                        resultsDocIds.append(list(self.index.items.get(templist[i]).get('posting').keys()))
                i = i + 1
            print(reduce(np.intersect1d, resultsDocIds))


    def vectorQuery(self, k):
        ''' vector query processing, using the cosine similarity. '''
        #ToDo: return top k pairs of (docID, similarity), ranked by their cosine similarity with the query in the descending order
        # You can use term frequency or TFIDF to construct the vectors



def test():
    ''' test your code thoroughly. put the testing cases here'''
    print('Pass')

def query():
    ''' the main query processing program, using QueryProcessor'''

    # ToDo: the commandline usage: "echo query_string | python query.py index_file processing_algorithm"
    # processing_algorithm: 0 for booleanQuery and 1 for vectorQuery
    # for booleanQuery, the program will print the total number of documents and the list of docuement IDs
    # for vectorQuery, the program will output the top 3 most similar documents

    qrys = loadCranQry('query.text')
#    for q in qrys:
#        print(q, qrys[q].text)

    loadiindex = InvertedIndex()
    loadiindex = loadiindex.load("index_file.json")
#    print("index loaded")

    cf = CranFile('cran.all')

    queryProcessor = QueryProcessor(qrys, loadiindex, cf.docs)
    queryProcessor.preprocessing()
    results = queryProcessor.booleanQuery()

if __name__ == '__main__':
    #test()
    query()
