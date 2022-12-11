import json
import random

# ----- MONGO DB ----- #
from pymongo import MongoClient


# ----- DATA STRUCTURES ----- #
from myapp.search.objects import Conection
from myapp.search.objects import Query



class AnalyticsData:
    """
    An in memory persistence object.
    Declare more variables to hold analytics tables.
    """
    # Connect to database server (local)
    mongodb = MongoClient('mongodb://localhost:27017/')
    print(mongodb.server_info())
    # Get database info
    db = mongodb['search_engine']
    # Get collections
    db_session = db['session']
    db_queries = db['queries']
    db_clicks = db['clicks']
    db_request = db['request']
    db_connections = db['connections']


    ### --------- CONNECTIONS COLLECTION --------- ###
    new_connections = []

    def add_connection(self, ip, country, city, browser, date):
        '''
        Creates a connection instance an adds it to the list of new connections
        '''

        print("adding new connection...")
        connection_info = Conection(ip, country, city, browser, date)
        print(connection_info.to_json())
        self.new_connections.append(connection_info)

        return connection_info

    def connections_post(self):
        '''
        Inserts the connections list into the database
        '''

        connections_list = [connection.to_json() for connection in self.new_connections]
        self.new_connections = []
        self.db_connections.insert_many(connections_list)

    def connections_get(self, query={}):
        '''
        Returns a list of connections based on the query sent
        '''


        return self.db_connections.find(query)
    
    ### -------------------------------------- ###
    ### --------- QUERIES COLLECTION --------- ###
    new_queries = []

    def add_query(self, query_id, query, query_length, results, city, country, ranking_method, browser, date):
        '''
        Creates a query instance an adds it to the list of new connections
        '''
        print("adding new query...")
        query_info = Query(query_id, query, query_length, results, city, country, ranking_method, browser, date)
        print(query_info.to_json())
        self.new_queries.append(query_info)

        return query_info

    def query_post(self):
        '''
        Inserts the queries list into the database
        '''

        queries_list = [query.to_json() for query in self.new_queries]
        self.new_queries = []
        self.db_queries.insert_many(queries_list)

    def query_get(self, query={}):
        '''
        Returns a list of queries based on the query sent
        '''


        return self.db_queries.find(query)

    ### -------------------------------------- ###

    """
    Ideas :)
    
    For users:
        - #users
        - browser the use
        - ip -> then city, country
    
    For the session:
        - time spent on the search engine -> difficult (pq es al cerrar?¿)
        - time of the day
        - dwell time --> dificil (to chungo pero ida de olla si lo conseguimos)
    
    For queries:
        - query_length
        - the query itself
        - extract "topic" of the query (si lo conseguimos somos Baki)
        - make a dictionnary like a count of terms in queries 
    
    For documents:
        - Number of times they have been ranked like relevant
        - Number of time they have been clicked

    Key thing is: when should each be stored? when should we call the method to store it?

    """
    # statistics table 1
    # fact_clicks is a dictionary with the click counters: key = doc id | value = click counter
    fact_clicks = dict([])

    # statistics table 2
    fact_two = dict([])

    # statistics table 3
    fact_three = dict([])

    ###########################
    #For the documents -> called when ranked, and called when clicked
    fact_relevant_documents_count = dict([]) #key = doc.id | value = count when ranked like relevant
    fact_clicked_documents_count = dict([]) #key = doc.id | value = count when ranked like relevant
    def add_fact_relevant_documents_count(self, doc_id):
        if doc_id not in self.fact_relevant_documents_count.keys():
            self.add_fact_relevant_documents_count[doc_id] = 1
        else:
            self.add_fact_relevant_documents_count[doc_id] += 1  
    def add_fact_clicked_documents_count(self, doc_id):
        if doc_id not in self.fact_clicked_documents_count.keys():
            self.add_fact_clicked_documents_count[doc_id] = 1
        else:
            self.add_fact_clicked_documents_count[doc_id] += 1  
    ###########################


    def save_query_terms(self, terms: str) -> int:
        print(self)
        return random.randint(0, 100000)


class ClickedDoc:
    def __init__(self, doc_id, description, counter):
        self.doc_id = doc_id
        self.description = description
        self.counter = counter

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)
