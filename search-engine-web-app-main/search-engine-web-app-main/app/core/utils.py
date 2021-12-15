import datetime
from random import random
import json
from faker import Faker

fake = Faker()


# fake.date_between(start_date='today', end_date='+30d')
# fake.date_time_between(start_date='-30d', end_date='now')
#
# # Or if you need a more specific date boundaries, provide the start
# # and end dates explicitly.
# start_date = datetime.date(year=2015, month=1, day=1)
# fake.date_between(start_date=start_date, end_date='+30y')

def get_random_date():
    """Generate a random datetime between `start` and `end`"""
    return fake.date_time_between(start_date='-30d', end_date='now')


def get_random_date_in(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())), )


class Document:
    def __init__(self, id, id_json, title, description, doc_date, username):
        self.id = id
        self.id_json = id_json
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.username = username
        #self.url = url
        #self.ip = ip
        


def load_documents_corpus():  # engine?
    """
    Load documents corpus from dataset_tweets_WHO.txt file
    :return:
    """

    ##### demo replace ith your code here #####
    
    with open('dataset_tweets_WHO.txt') as f:
       json_data = json.load(f)
    
    
    docs = []
   
    for i in range(len(json_data)):
        idd = i
        id2 = json_data[str(i)]['id_str'] #long id
        titlee = json_data[str(i)]['full_text'][:100]
        desc = json_data[str(i)]['full_text']
        date = json_data[str(i)]['created_at']
        user = json_data[str(i)]['user']['name']
        #urll = 'doc_details?title={}&date={}'
        
        docs.append(Document(id = idd, id_json = id2, title = titlee, description = desc, doc_date = date, username = user))
    
    return docs
    
