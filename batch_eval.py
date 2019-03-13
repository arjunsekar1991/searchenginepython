'''
a program for evaluating the quality of search algorithms using the vector model

it runs over all queries in query.text and get the top 10 results,
and then qrels.text is used to compute the NDCG metric

usage:
    python batch_eval.py index_file query.text qrels.text

    output is the average NDCG over all the queries


'''
import random
from functools import reduce
from query import query
from cranqry import loadCranQry
from index import InvertedIndex
from cran import CranFile
from metrics import ndcg_score
import numpy as np
def eval(numberofrandomqueries):

    # ToDo
    actual = []
   #
    qrys = loadCranQry("query.text")
    validqueries = []
    for q in qrys:
        validqueries.append(int(q))

    loadiindex = InvertedIndex()
    loadiindex = loadiindex.load("index_file")
    #    print("index loaded")
    cf = CranFile('cran.all')
    #QueryProcessor.numberofresult =10
    #qp = QueryProcessor(qrys,loadiindex,cf.docs,10)
    queryRelevence = dict()
    for line in open("qrels.text"):

        fields = line.split(" ")
        fields[0] = '%0*d' % (3, int(fields[0]))
        if fields[0] in queryRelevence:
            # and let's extract the data:
            queryRelevence[fields[0]].append(fields[1])
        else:
            # create a new array in this slot
            queryRelevence[fields[0]] = [fields[1]]


    relevent = list(queryRelevence.keys())
    relevent = list(map(int, relevent))
    samplespace = np.intersect1d(relevent, validqueries)
    list_of_random_items = random.sample(list(samplespace), numberofrandomqueries)
    tempcounter2 = 0

    while tempcounter2<numberofrandomqueries:

        list_of_random_items[tempcounter2] = '%0*d' % (3, int(list_of_random_items[tempcounter2]))
        print('query for which ndcg is calculated '+ str(list_of_random_items[tempcounter2]))
        y = str(list_of_random_items[tempcounter2])
        vectorresult = query('index_file', '1', 'query.text', '105', 10)
        tempcounter =0
        for k in vectorresult:

            if k in queryRelevence[str(list_of_random_items[tempcounter2])]:
                vectorresult[tempcounter]=1
            else:
                vectorresult[tempcounter]=0
            tempcounter = tempcounter + 1
        #print(vectorresult)
        idealvectorresult = vectorresult.copy()
        idealvectorresult.sort(reverse=True)
        #print(idealvectorresult)
        if sum(idealvectorresult) == 0:
            ndcgscore = 0
        else:
            ndcgscore = ndcg_score(idealvectorresult,vectorresult)
        print(ndcgscore)
        print('Done')
        tempcounter2 = tempcounter2 - 1

if __name__ == '__main__':
    eval(3)
