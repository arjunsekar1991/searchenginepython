
'''

Index structure:

    The Index class contains a list of IndexItems, stored in a dictionary type for easier access

    each IndexItem contains the term and a set of PostingItems

    each PostingItem contains a document ID and a list of positions that the term occurs

'''
import util
import re
# import doc
from cran import CranFile
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP

import json, codecs
import jsonpickle
class Posting:
    def __init__(self, docID):
        self.docID = docID
        self.positions = []

    def append(self, pos):
        self.positions.append(pos)

    def sort(self):
        ''' sort positions'''
        self.positions.sort()

    def merge(self, positions):
        self.positions.extend(positions)

    def term_freq(self):
        ''' return the term frequency in the document'''
        # ToDo


class IndexItem:
    def __init__(self, term):
        self.term = term
        self.posting = {}  # postings are stored in a python dict for easier index building
        #self.sorted_posting s= [] # may sort them by docID for easier query processing

    def add(self, docid, pos):
        ''' add a posting'''
        if docid not in self.posting:
            self.posting[docid] = Posting(docid)
        self.posting[docid].append(pos)

    def sort(self):
        ''' sort by document ID for more efficient merging. For each document also sort the positions'''
        # ToDo


class InvertedIndex:

    def __init__(self):
        self.items = {} # list of IndexItems
        self.nDocs = 0  # the number of indexed documents


    def indexDoc(self, doc): # indexing a Document object
        ''' indexing a docuemnt, using the simple SPIMI algorithm, but no need to store blocks due to the small collection we are handling. Using save/load the whole index instead'''

        # ToDo: indexing only title and body; use some functions defined in util.py
        # (1) convert to lower cases,
        # (2) remove stopwords,
        # (3) stemming
        processData = []
        indexitemlist = []
#        if doc.docID == '1':
#            print(doc.docID)
        titletoken = re.split(" ", doc.title.replace('\n', ' '))
        titletoken = ' '.join(titletoken).split()
        bodytoken = re.split(" ", doc.body.replace('\n', ' '))
        bodytoken = ' '.join(bodytoken).split()
        tokens = titletoken + bodytoken
        tokens = [element.lower() for element in tokens];
# print (tokens)
# capturing useful information before preprocessing and stemming
        k = 0
        positionindoc = 1
        while k < len(tokens):
#                print(tokens[k])
                tuple = (doc.docID, tokens[k] ,positionindoc)

                processData.append(tuple)
                tempindexitem = IndexItem(tokens[k])
                isaddable = None
                if k == 0:
                    tempindexitem.add(doc.docID, positionindoc)
                    indexitemlist.append(tempindexitem)
                for x in indexitemlist:
                    if x.term != tokens[k]:
                        isaddable = True
                    else:
                        if k!= 0:
                            isaddable = False
                            x.posting.get(doc.docID).append(positionindoc)
                        break
                if isaddable:

                    tempindexitem.add(doc.docID,positionindoc)
                    indexitemlist.append(tempindexitem)


                positionindoc = positionindoc + len(tokens[k]) + 1;
                k = k + 1

            #            print (processData[0])
            #            print (processData[1])
            #            print (processData[2])
            #            print (doc.title[:12])
#        print(indexitemlist)
        self.items = indexitemlist
        self.save("index_file")

    def sort(self):
        ''' sort all posting lists by docID'''
        # ToDo

    def find(self, term):
        return self.items[term]

    def save(self, filename):
        ''' save to disk'''
        # ToDo: using your preferred method to serialize/deserialize the index
        jsonEncoded = jsonpickle.encode(self.items)
  #      print(jsonEncoded)
        fh = open(filename, 'a')
        fh.write(jsonEncoded)
        fh.close

    def load(self, filename):
        ''' load from disk'''
        # ToDo

    def idf(self, term):
        ''' compute the inverted document frequency for a given term'''
        # ToDo: return the IDF of the term

    # more methods if needed


def test():
    ''' test your code thoroughly. put the testing cases here'''
    print('Pass')


def indexingCranfield():
    # ToDo: indexing the Cranfield dataset and save the index to a file
    # command line usage: "python index.py cran.all index_file"
    # the index is saved to index_file
    cf = CranFile('cran.all')
    iindex = InvertedIndex()
    for doc in cf.docs:
        iindex.indexDoc(doc)
    #print(iindex.items)


if __name__ == '__main__':
    # test()
    indexingCranfield()
