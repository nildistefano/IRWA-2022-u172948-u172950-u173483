from collections import defaultdict
import math
import json
import numpy as np
import pandas as pd
from os.path import join

def create_index_tfidf(dataframe):
    """
    Implement the inverted index and compute tf, df and idf
    
    Argument:
    dataframe -- DataFrame containing tweet information
    
    Returns:
    index - the inverted index (implemented through a Python dictionary) containing terms as keys and the corresponding
    list of document these keys appears in (and the positions) as values.
    tf - normalized term frequency for each term in each document
    df - number of documents each term appear in
    idf - inverse document frequency of each term
    """

    num_documents = dataframe.shape[0]
    index = defaultdict(list)
    tf = defaultdict(list)  # term frequencies of terms in documents (documents in the same order as in the main index)
    df = defaultdict(int)   # document frequencies of terms in the corpus
    idf = defaultdict(float)
    for row in dataframe.iterrows():
        doc_id = row[1]['Document']
        terms = row[1]['Clean_text']  
        terms = eval(terms)

        current_page_index = {}

        for position, term in enumerate(terms):  ## terms contains page_title + page_text
            try:
                # if the term is already in the dict append the position to the corresponding list
                current_page_index[term][1].append(position) 
            except:
                # Add the new term as dict key and initialize the array of positions and add the position
                current_page_index[term]=[doc_id, [position]]
                
        #normalize term frequencies
        # Compute the denominator to normalize term frequencies (formula 2 above)
        # norm is the same for all terms of a document.
        norm = 0
        for term, posting in current_page_index.items():
            # posting will contain the list of positions for current term in current document. 
            # posting ==> [current_doc, [list of positions]] 
            # you can use it to infer the frequency of current term.
            norm += len(posting[1]) ** 2
        norm = math.sqrt(norm)

        # calculate the tf(dividing the term frequency by the above computed norm) and df weights
        for term, posting in current_page_index.items():
            # append the tf for current term (tf = term frequency in current doc/norm)
            tf[term].append(np.round(len(posting[1])/norm,4)) ## SEE formula (1) above
            #increment the document frequency of current term (number of documents containing the current term)
            df[term] = df[term]+1 # increment DF for current term

        #merge the current page index with the main index
        for term_page, posting_page in current_page_index.items():
            index[term_page].append(posting_page)

        # Compute IDF following the formula (3) above. HINT: use np.log
        for term in df:
            idf[term] = np.round(np.log(float(num_documents/df[term])), 4)

    return index, tf, df, idf

def load_index_tfidf(path):

    with open(join(path,'index.json'), 'r') as fp:
        index = json.load(fp)

    with open(join(path,'tf.json'), 'r') as fp:
        tf = json.load(fp)

    with open(join(path,'df.json'), 'r') as fp:
        df = json.load(fp)
    
    with open(join(path,'idf.json'), 'r') as fp:
        idf = json.load(fp)
    
    return index, tf, df, idf


def save_index_tfidf(index, tf, df, idf, path):

    with open(join(path,'index.json'), 'w') as fp:
        json.dump(index, fp)

    with open(join(path,'tf.json'), 'w') as fp:
        json.dump(tf, fp)

    with open(join(path,'df.json'), 'w') as fp:
        json.dump(df, fp)
    
    with open(join(path,'idf.json'), 'w') as fp:
        json.dump(idf, fp)