import random

from myapp.search.objects import ResultItem, Document
from myapp.search.aux_functions import search_tf_idf

def build_results(corpus, search_id, search_query, index, ranking, idf, tf, docu_length) :
    """
    PRE: corpus (dictionnary of Documents, key=doc_id), search_id, search_query (example: "Weather Kansas"),
    index (inverted_index of your documents), ranking (ranking method, example: "bm25"), idf, tdf
    docu_length (dictionnary where keys=doc_id and value=doc_length)
    ---------------------------------------------------------------
    POST: a list of demo docs sorted by ranking
    """
    res = []
    ranked_docs = search_tf_idf(search_query, index, ranking, idf, tf, docu_length)
    for doc in ranked_docs[:10]:
        rank = doc[0]
        id = doc[1]
        item = corpus[id]
        res.append(ResultItem(item.id, item.title, item.description, item.doc_date,
                              "doc_details?id={}&search_id={}&param2=2".format(item.id, search_id), random.random()))

    #sort by ranking
    res.sort(key=lambda doc: doc.ranking, reverse=True)
    return res



class SearchEngine:
    #Our search function
    def search(self, corpus, search_id, search_query, index, ranking, idf, tf, docu_length):
        print("Search query:", search_query)
        results = build_results(corpus, search_id, search_query, index, ranking, idf, tf, docu_length) 
        return results
