import os
from json import JSONEncoder
from datetime import datetime

# pip install httpagentparser
import httpagentparser  # for getting the user agent as json
import nltk
import flask
import json
import pandas as pd
from flask import Flask, render_template, session
from flask import request

from myapp.analytics.analytics_data import AnalyticsData, ClickedDoc
from myapp.search.load_corpus import load_corpus
from myapp.search.objects import Document, StatsDocument
from myapp.search.search_engine import SearchEngine

# ----- FUNCIONES AUXILIARES ----- #
from myapp.search.aux_functions import create_index_tfidf
from myapp.search.aux_functions import load_index_tfidf
from myapp.search.aux_functions import save_index_tfidf

# ----- MONGO DB ----- #
from pymongo import MongoClient
# Connect to database server (local)
mongodb = MongoClient('mongodb://localhost:27017/')
print(mongodb.server_info())
# Get database info
db = mongodb['search_engine']
# Get collections
db_session = db['session']
db_clicks = db['clicks']
db_request = db['request']

# *** for using method to_json in objects ***
def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default

# end lines ***for using method to_json in objects ***

# instantiate the Flask application
app = Flask(__name__)

# random 'secret_key' is used for persisting data in secure cookie
app.secret_key = 'afgsreg86sr897b6st8b76va8er76fcs6g8d7'
# open browser dev tool to see the cookies
app.session_cookie_name = 'IRWA_SEARCH_ENGINE'

# instantiate our search engine
search_engine = SearchEngine()

# instantiate our in memory persistence
analytics_data = AnalyticsData()


# print("current dir", os.getcwd() + "\n")
# print("__file__", __file__ + "\n")
full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)
# print(path + ' --> ' + filename + "\n")
# load documents corpus into memory.
file_path = path + "/tw_hurricane_data.json"

# file_path = "../../tweets-data-who.json"
corpus = load_corpus(file_path) #We get a dictionnary key=doc_id, values-> <class 'myapp.search.objects.Document'>
#If you want to get a document title you should do corpus[id].title


# # CARGAMOS EL ÍNDICE INVERSO #
index_path = path + "/lab_material/"
try:
     our_index, tf, df, idf = load_index_tfidf(index_path)
except:
     print("Index not found into local storage: Creating a new index")
     our_index, tf, df, idf = create_index_tfidf(corpus)
     save_index_tfidf(our_index, tf, df, idf, index_path)

#creating docu_length
docu_length = dict()
for doc in corpus.values():
    docu_length[doc.id] = len(doc.description)

tweet_info = {}
for doc in corpus.values():
    tweet_info[doc.id] = (doc.hashtags, doc.likes, doc.retweets) 

# Home URL "/"
@app.route('/')
def index():
    print("starting home url /...")
    # flask server creates a session by persisting a cookie in the user's browser.
    # the 'session' object keeps data between multiple requests
    print(session.keys())
    if 'first_connection' not in session.keys():
        session['first_connection'] = datetime.now()
        print("First session connection...")
        # Analytics for the user
        #...Getting the data
        browser = request.headers.get('User-Agent') #esto hay que gestionarlo que da un string raro
        ip = request.remote_addr
        country = "Spain" #get country from IP
        city = "Barcelona" #get city from IP
        #...Storing the data
        analytics_data.add_connection(ip=ip, country=country, city=city, browser=browser, date=datetime.utcnow())
        analytics_data.connections_post()
        # Analytics of the session
        #...Getting the data
        local_time = str(datetime.now())
        #...Storing the data
        #analytics_data.add_fact_time_of_day(local_time)

        # Other stuf...
        #agent = httpagentparser.detect(browser)
        #print("Remote IP: {} - JSON user browser {}".format(ip, agent))
        just_entered = False #so it is not filled again
        
    print(session)

    return render_template('index.html', page_title="Welcome")


@app.route('/search', methods=['POST'])
def search_form_post():
    search_query = request.form['search-query']
    ranking_method = request.form['ranking']

    session['last_search_query'] = search_query

    search_id = analytics_data.save_query_terms(search_query)

    #results = search_engine.search(search_query, search_id, corpus)
    # ranking_method = "tf-idf_cosine-similarity"
    # #ranking_method = "bm25"
    results = search_engine.search(corpus, search_id, search_query, our_index, ranking_method, idf, tf, docu_length, tweet_info)

    found_count = len(results)
    session['last_found_count'] = found_count
    print('\n\n')
    print(results)

    browser = request.headers.get('User-Agent') #esto hay que gestionarlo que da un string raro
    country = "Spain" #get country from IP
    city = "Barcelona" #get city from IP

    #Save analytics
    analytics_data.add_query(query_id=search_id, query=search_query, query_length=len(search_query), results='', city=city, country=country, ranking_method=ranking_method, browser=browser, date=datetime.utcnow())
    analytics_data.query_post()
    print(session)

    return render_template('results.html', results_list=results, page_title="Results", found_counter=found_count)


@app.route('/doc_details', methods=['GET'])
def doc_details():
    # getting request parameters:
    # user = request.args.get('user')

    print("doc details session: ")
    print(session)

    res = session["some_var"]

    print("recovered var from session:", res)

    # get the query string parameters from request
    clicked_doc_id = request.args["id"]
    p1 = int(request.args["search_id"])  # transform to Integer
    print("click in id={}".format(clicked_doc_id))

    doc = search_engine.get_doc(corpus, request.args["id"])

    # store data in statistics table 1
    if clicked_doc_id in analytics_data.fact_clicks.keys():
        analytics_data.fact_clicks[clicked_doc_id] += 1
    else:
        analytics_data.fact_clicks[clicked_doc_id] = 1

    print("fact_clicks count for id={} is {}".format(clicked_doc_id, analytics_data.fact_clicks[clicked_doc_id]))

    return render_template('doc_details.html', doc=doc, page_title="Tweet: {}".format(doc.id))


@app.route('/stats', methods=['GET'])
def stats():
    """
    Show simple statistics example. ### Replace with dashboard ###
    :return:
    """

    docs = []
    # ### Start replace with your code ###

    for doc_id in analytics_data.fact_clicks:
        row: Document = corpus[int(doc_id)]
        count = analytics_data.fact_clicks[doc_id]
        doc = StatsDocument(row.id, row.title, row.description, row.doc_date, row.url, count)
        docs.append(doc)

    # simulate sort by ranking
    docs.sort(key=lambda doc: doc.count, reverse=True)
    return render_template('stats.html', clicks_data=docs)
    # ### End replace with your code ###


@app.route('/dashboard', methods=['GET'])
def dashboard():
    visited_docs = []
    for doc_id in analytics_data.fact_clicks:
        d: Document = corpus[int(doc_id)]
        doc = ClickedDoc(doc_id, d.description, analytics_data.fact_clicks[doc_id])
        visited_docs.append(doc)

    # simulate sort by ranking
    visited_docs.sort(key=lambda doc: doc.counter, reverse=True)
    visited_ser=[]
    for doc in visited_docs:
        visited_ser.append(doc.to_json())

    queries = []
    for query in analytics_data.query_get():
        queries.append(query['query'])

    countries = []
    for connection in analytics_data.connections_get():
        countries.append(connection['country'])
    
    countries_count = {}
    for country in countries:
        if country in countries_count.keys():
            countries_count[country] += 1
        else:
            countries_count[country] = 1

    return render_template('dashboard.html', visited_docs=visited_ser, queries=queries, countries=json.dumps(countries_count))


@app.route('/sentiment')
def sentiment_form():
    return render_template('sentiment.html')


@app.route('/sentiment', methods=['POST'])
def sentiment_form_post():
    text = request.form['text']
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    score = ((sid.polarity_scores(str(text)))['compound'])
    return render_template('sentiment.html', score=score)


if __name__ == "__main__":
    app.run(port=8088, host="0.0.0.0", threaded=False, debug=True) 