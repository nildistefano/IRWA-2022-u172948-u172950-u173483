from collections import defaultdict
import math
import json
import numpy as np
import pandas as pd
from os.path import join
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from collections import defaultdict
import collections
import numpy as np
from numpy import linalg as la


def create_index_tfidf(corpus):
    """
    Implement the inverted index and compute tf, df and idf
    
    Argument:
    corpus --> dictionnary of Documents (Document object), key=doc_id
    
    Returns:
    index - the inverted index (implemented through a Python dictionary) containing terms as keys and the corresponding
    list of document these keys appears in (and the positions) as values.
    tf - normalized term frequency for each term in each document
    df - number of documents each term appear in
    idf - inverse document frequency of each term
    """

    num_documents = len(corpus)
    index = defaultdict(list)
    tf = defaultdict(list)  # term frequencies of terms in documents (documents in the same order as in the main index)
    df = defaultdict(int)   # document frequencies of terms in the corpus
    idf = defaultdict(float)
    for doc in corpus.values():
        doc_id = doc.id
        terms = build_terms(doc.description)
        print("Doc_id: ",doc_id)
        print("Terms: ", terms)

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



def build_terms(line):
    """
    Preprocess the article text (title + body) removing stop words, stemming,
    transforming in lowercase and return the tokens of the text.
    
    Argument:
    line -- string (text) to be preprocessed
    
    Returns:
    line - a list of tokens corresponding to the input text after the preprocessing
    """

    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    ## START CODE
    line=  line.lower() ## Transform in lowercase
    line=  line.split() ## Tokenize the text to get a list of terms
    line= [x for x in line if x not in stop_words]  ##eliminate the stopwords (HINT: use List Comprehension)
    line= [stemmer.stem(x) for x in line] ## perform stemming (HINT: use List Comprehension)
    ## END CODE
    return line

def rank_documents_bm25(terms, docs, index, idf, tf, k1, b, N, docu_length, lavg):
    """
    Perform the ranking of the results of a search based on bm25
    
    Argument:
    terms -- list of query terms
    docs -- list of documents, to rank, matching the query
    index -- inverted index data structure
    idf -- inverted document frequencies
    tf -- term frequencies
    k1, b -- weighting terms for normalization
    N -- number of documents
    docu_length -- dictionnary with key=doc_id, value=len(doc with doc_id)
    lavg -- average length
    
    Returns:
    list of ranked documents
    """

    # I'm interested only on the element of the docVector corresponding to the query terms 
    # The remaining elements would became 0 when multiplied to the query_vector
    doc_vectors = defaultdict(lambda: [0] * len(terms)) # I call doc_vectors[k] for a nonexistent key k, the key-value pair (k,[0]*len(terms)) will be automatically added to the dictionary


    for termIndex, term in enumerate(terms):  #termIndex is the index of the term in the query
        print(term)
        if term not in index.keys():
            continue
        
        # Generate doc_vectors for matching docs
        for doc_index, (doc, postings) in enumerate(index[term]):         
            if doc in docs:
                dft = len(index[term]) #in how many documents does it appear
                ld = docu_length[doc] #document length
                doc_vectors[doc][termIndex] = np.log(N/dft) * (((k1+1)*tf[term][doc_index]) / (k1*((1-b)+b*( ld / lavg ) ) + tf[term][doc_index]))
    
    # Calculate the score of each doc (the sum of the results)    
    doc_scores=[[np.sum(curDocVec), doc] for doc, curDocVec in doc_vectors.items() ]
    doc_scores.sort(reverse=True)
    #print document titles instead if document id's
    #result_docs=[ title_index[x] for x in result_docs ]
    if len(doc_scores) == 0:
        print("No results found for query")
    #print ('\n'.join(result_docs), '\n')
    return doc_scores

def rank_documents_dedicated(terms, docs, index, idf, tf, k1, b, N, docu_length, lavg, info):
    """
    Perform the ranking of the results of a search based on the tf-idf weights
    
    Argument:
    terms -- list of query terms
    docs -- list of documents, to rank, matching the query
    index -- inverted index data structure
    idf -- inverted document frequencies
    tf -- term frequencies
    info -- Info that will be used to add puntuation to the document
    
    Returns:
    list of ranked documents
    """

    # I'm interested only on the element of the docVector corresponding to the query terms 
    # The remaining elements would became 0 when multiplied to the query_vector
    doc_vectors = defaultdict(lambda: [0] * len(terms)) # I call doc_vectors[k] for a nonexistent key k, the key-value pair (k,[0]*len(terms)) will be automatically added to the dictionary


    for termIndex, term in enumerate(terms):  #termIndex is the index of the term in the query
        if len(index[term])==0:
            continue
        
        # Generate doc_vectors for matching docs
        for doc_index, (doc, postings) in enumerate(index[term]):         
            if doc in docs:
                dft = len(index[term]) #in how many documents does it appear
                ld = docu_length[doc] #document length
                doc_vectors[doc][termIndex] = np.log(N/dft) * (((k1+1)*tf[term][doc_index]) / (k1*((1-b)+b*( ld / lavg ) ) + tf[term][doc_index]))
    
    # Calculate the score of each doc (the sum of the results)    
    doc_scores=[[np.sum(curDocVec), doc] for doc, curDocVec in doc_vectors.items() ]
    doc_scores = []
    doc_scores_info = []

    for doc, curDocVec in doc_vectors.items():
        # BM score
        bm_score = np.sum(curDocVec)
        # Hashtag score
        h_score = len([term for term in terms if term.lower() in [x.lower() for x in info[info['Document'] == doc]['Hashtags']]])/len(terms)
        # Likes score
        l_score = math.log(1+(info[info['Document'] == doc]['Likes']/1 + info['Likes'].max()))
        # Retweets score
        r_score = math.log(1+(info[info['Document'] == doc]['Retweets']/1 + info['Retweets'].max()))
        # Relevance score
        relevance_score = 0.4 * h_score + 0.3 * l_score + 0.3 * r_score
        # Dedicated score
        total_score = bm_score * (1+relevance_score)/relevance_score
        doc_scores.append([total_score, doc])
        doc_scores_info.append([bm_score, h_score, l_score, r_score, doc])


    doc_scores.sort(reverse=True)
    #print document titles instead if document id's
    #result_docs=[ title_index[x] for x in result_docs ]
    if len(doc_scores) == 0:
        print("No results found for query")
    #print ('\n'.join(result_docs), '\n')
    return doc_scores, doc_scores_info

#Let's keep that as a reference
def rank_documents(terms, docs, index, idf, tf):
    """
    Perform the ranking of the results of a search based on the tf-idf weights
    
    Argument:
    terms -- list of query terms
    docs -- list of documents, to rank, matching the query
    index -- inverted index data structure
    idf -- inverted document frequencies
    tf -- term frequencies
    
    Returns:
    list of ranked documents
    """

    # I'm interested only on the element of the docVector corresponding to the query terms 
    # The remaining elements would became 0 when multiplied to the query_vector
    doc_vectors = defaultdict(lambda: [0] * len(terms)) # I call doc_vectors[k] for a nonexistent key k, the key-value pair (k,[0]*len(terms)) will be automatically added to the dictionary
    query_vector = [0] * len(terms)

    # compute the norm for the query tf
    query_terms_count = collections.Counter(terms)  # get the frequency of each term in the query. 

    query_norm = la.norm(list(query_terms_count.values()))

    for termIndex, term in enumerate(terms):  #termIndex is the index of the term in the query
        if term not in index:
            continue

        ## Compute tf*idf(normalize TF as done with documents)
        query_vector[termIndex]=query_terms_count[term]/query_norm *idf[term]

        # Generate doc_vectors for matching docs
        for doc_index, (doc, postings) in enumerate(index[term]):

            #tf[term][0] will contain the tf of the term "term" in the doc 26            
            if doc in docs:
                doc_vectors[doc][termIndex] = tf[term][doc_index] * idf[term]
    
    # Calculate the score of each doc 
    # compute the cosine similarity between queyVector and each docVector:
    
    doc_scores=[[np.dot(curDocVec, query_vector), doc] for doc, curDocVec in doc_vectors.items() ]
    doc_scores.sort(reverse=True)
    #print document titles instead if document id's
    #result_docs=[ title_index[x] for x in result_docs ]
    if len(doc_scores) == 0:
        print("No results found for query")
    #print ('\n'.join(result_docs), '\n')
    return doc_scores



def search_tf_idf(query, index, ranking, idf, tf, docu_length):
    """
    output is the list of documents that contain any of the query terms. 
    So, we will get the list of documents for each query term, and take the union of them.
    """
    #getting average length
    lavg = 0
    for length in docu_length.values():
        lavg += length
    lavg = round(lavg / len(docu_length))
    ###

    query = build_terms(query)
    docs = set()
    for term in query:
        try:
            # store in term_docs the ids of the docs that contain "term"                        
            term_docs=[posting[0] for posting in index[term]]
            
            # docs = docs Union term_docs
            docs = docs.union(term_docs)
        except:
            #term is not in index
            pass
    docs = list(docs)
    if (ranking == "bm25"):
        ranked_docs = rank_documents_bm25(query, docs, index, idf, tf, k1 = 1.6, b = 0.75, N = len(docu_length), docu_length = docu_length, lavg=lavg) #TO-DO new formula!! (new function, new attributes)
    elif ranking == "dedicated":
        ranked_docs, _ = rank_documents_dedicated(query, docs, index, idf, tf, k1 = 1.6, b = 0.75, N = len(docu_length), docu_length = docu_length, lavg = lavg, info=data[['Document', 'Hashtags', 'Likes', 'Retweets']]) 
    elif (ranking == "tf-idf_cosine-similarity"):
        ranked_docs = rank_documents(query, docs, index, idf, tf)
    else:
        print("Something went wrong")
    return ranked_docs