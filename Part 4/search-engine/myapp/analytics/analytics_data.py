import json
import random


class AnalyticsData:
    """
    An in memory persistence object.
    Declare more variables to hold analytics tables.
    """


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
    #For users -> called when initializing the session!
    fact_browser = dict([]) #key = browser | value = count
    fact_ip = [] #list of IPs (maybe we should use a dict with some sort of key...)
    fact_city = dict([]) #key = city | value = count
    fact_country = dict([]) #key = country | value = count

    def add_fact_browser(self, browser):
        if browser not in self.fact_browser.keys():
            self.fact_browser[browser] = 1
        else:
            self.fact_browser[browser] += 1

    def add_fact_ip(self, ip):
        self.fact_ip.append(ip)
    
    def add_fact_city(self, city):
        if city not in self.fact_city.keys():
            self.fact_city[city] = 1
        else:
            self.fact_city[city] += 1
    
    def add_fact_country(self, country):
        if country not in self.fact_country.keys():
            self.fact_country[country] = 1
        else:
            self.fact_country[country] += 1
    ###########################

    ###########################
    #For the session -> called when entering the sesstion
    fact_time_of_day = [] #list of times of the day when people entered (maybe we should use a dict with some sort of key...)
    def add_fact_time_of_day(self, time_of_day):
        self.fact_time_of_day = time_of_day
    ###########################

    ###########################
    #For the queries -> called when /search is called 
    fact_query_length = [] #list of query lengths
    fact_query = dict([]) #key = query | value = count
    fact_terms_count = dict([]) #key = term | value = count
    def add_fact_query_length(self, length):
        self.fact_query_length = length
    def add_fact_query(self, query):
        if query not in self.fact_query.keys():
            self.fact_query[query] = 1
        else:
            self.fact_query[query] += 1
    def add_fact_terms_count(self, term):
        if term not in self.fact_terms_count.keys():
            self.fact_terms_count[term] = 1
        else:
            self.fact_terms_count[term] += 1
    ###########################

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
