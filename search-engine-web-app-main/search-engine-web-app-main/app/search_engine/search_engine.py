import random

from app.core.utils import get_random_date
from app.core.utils import load_documents_corpus
from app.search_engine.algorithms import create_index_tfidf
from app.search_engine.algorithms import search_tf_idf


def build_demo_data():
    """
    Helper method, just to demo the app
    :return: a list of demo docs sorted by ranking
    """
    samples = ["Messier 81", "StarBurst", "Black Eye", "Cosmos Redshift", "Sombrero", "Hoags Object",
            "Andromeda", "Pinwheel", "Cartwheel",
            "Mayall's Object", "Milky Way", "IC 1101", "Messier 87", "Ring Nebular", "Centarus A", "Whirlpool",
            "Canis Major Overdensity", "Virgo Stellar Stream"]

    res = []
    for index, item in enumerate(samples):
        res.append(DocumentInfo(item, (item + " ") * 5, get_random_date(),
                                "doc_details?id={}&param1=1&param2=2".format(index), random.random()))
    # simulate sort by ranking
    res.sort(key=lambda doc: doc.ranking, reverse=True)
    return res


class SearchEngine:
    """educational search engine"""
    
    def __init__(self, num_documents, corpus, index, tf, df, idf, title_index):
    
        #declare varriables
        #have already doc corpus to do the search
        #generate index
        self.corpus = corpus #load corpus
        self.num_documents = num_documents
        self.index = index
        self.tf = tf
        self.df = df
        self.idf = idf
        self.title_index = title_index

    def search(self, search_query):
        print("Search query:", search_query)
        
        #use above to do search (ranking.. -> get results list)
        ranked_docs, doc_scores = search_tf_idf(search_query, self.index, self.idf, self.tf, self.title_index)


        results = []
        
        for i in range(len(ranked_docs)):
            for tweet in self.corpus:
                if ranked_docs[i] == tweet.id:
                    #results.append(tweet)
            
                    results.append(DocumentInfo(tweet.id_json, tweet.title, tweet.description, tweet.doc_date,
                                "doc_details?id="+str(tweet.id_json)+"&title="+str(tweet.title)+"&date="+str(tweet.doc_date), i))
        return results



class DocumentInfo:
    def __init__(self, id, title, description, doc_date, url, ranking):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.url = url
        self.ranking = ranking

