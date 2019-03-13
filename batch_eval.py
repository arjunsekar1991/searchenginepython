'''
a program for evaluating the quality of search algorithms using the vector model

it runs over all queries in query.text and get the top 10 results,
and then qrels.text is used to compute the NDCG metric

usage:
    python batch_eval.py index_file query.text qrels.text

    output is the average NDCG over all the queries


'''

from query import query
from cranqry import loadCranQry
from index import InvertedIndex
from cran import CranFile
def eval():

    # ToDo
    actual = []
   #
    qrys = loadCranQry("query.text")
    #    for q in qrys:
    #        print(q, qrys[q].text)

    loadiindex = InvertedIndex()
    loadiindex = loadiindex.load("index_file")
    #    print("index loaded")
    cf = CranFile('cran.all')
    #QueryProcessor.numberofresult =10
    #qp = QueryProcessor(qrys,loadiindex,cf.docs,10)

    print(query('index_file', '1', 'query.text', '029', 10))
    print('Done')

if __name__ == '__main__':
    eval()
