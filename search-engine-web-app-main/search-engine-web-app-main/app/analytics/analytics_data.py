import json
import random


class AnalyticsData:
    """
    An in memory persistence object.
    Declare more variables to hold analytics tables.
    """
    
    def __init__(self, query_length):
        self.query_length = query_length
    
    # statistics table 1
    # fact_clicks is a dictionary with the click counters: key = doc id | value = click counter
    fact_clicks = dict([])

    # statistics table 2
    fact_two = dict([])

    # statistics table 3
    fact_three = dict([])
    
    #save query 


    def save_query_terms(self, terms: str) -> int:
        #print(self)
        t = terms.split()
        self.query_length = len(t)
        return random.randint(0, 100000)
        
        
    

class ClickedDoc:
    def __init__(self, doc_id, description, counter):
        self.doc_id = doc_id
        self.description = description
        self.counter = counter
        #self.queries = queries

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)
