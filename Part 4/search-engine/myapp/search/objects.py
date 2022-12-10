import json

class Conection:
    """
    Data analysis class to store visits information in visits collection

    ip → ip the connection is done from
    country → country of procedence
    city → city of procedence
    browser → browser used
    date → date of the connection
    """
   
    def __init__(self, ip, country, city, browser, date):
        self.ip = ip
        self.country = country
        self.city = city
        self.browser = browser
        self.date = date

    def to_json(self):
        return self.__dict__
    
    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)

class Query:
    """
    Data analysis class to store query information in queries collection

    query_id → id of the query
    query → text of the query
    results → results returned by the engine
    ip → ip the query was done from
    engine →  engine used to show results
    date → date of the query
    """

    def __init__(self, query_id, query, results, ip, engine, date):
        self.query_id = query_id
        self.query = query
        self.results = results
        self.ip = ip
        self.engine = engine
        self.date = date

    def to_json(self):
        return self.__dict__
    
    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)

class Document:
    """
    Original corpus data as an object
    """

    def __init__(self, id, title, description, doc_date, likes, retweets, url, hashtags):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.likes = likes
        self.retweets = retweets
        self.url = url
        self.hashtags = hashtags

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)


class StatsDocument:
    """
    Original corpus data as an object
    """

    def __init__(self, id, title, description, doc_date, url, count):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.url = url
        self.count = count

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)


class ResultItem:
    def __init__(self, id, title, description, doc_date, url, ranking):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.url = url
        self.ranking = ranking
