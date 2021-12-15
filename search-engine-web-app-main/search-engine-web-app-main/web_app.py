import os
from json import JSONEncoder

from datetime import datetime

import nltk
from flask import Flask, render_template, session
from flask import request

import httpagentparser  # for getting the user agent as json

from app.analytics.analytics_data import AnalyticsData, ClickedDoc
from app.core import utils
from app.search_engine.search_engine import SearchEngine

from app.core.utils import load_documents_corpus
from app.search_engine.algorithms import create_index_tfidf

# *** for using method to_json in objects ***
def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default


# instantiate the Flask application
app = Flask(__name__)

# random 'secret_key' is used for persisting data in secure cookie
app.secret_key = 'afgsreg86sr897b6st8b76va8er76fcs6g8d7'
# open browser dev tool to see the cookies
app.session_cookie_name = 'IRWA_SEARCH_ENGINE'

#####
corpus = load_documents_corpus() 
num_documents = len(corpus)
#print('before index')
index, tf, df, idf, title_index = create_index_tfidf(corpus, num_documents)
#print('after index')

searchEngine = SearchEngine(num_documents, corpus, index, tf, df, idf, title_index)
analytics_data = AnalyticsData(0)
#corpus = utils.load_documents_corpus()



@app.route('/')
def search_form():
    
    print("starting home url /...")

    # flask server creates a session by persisting a cookie in the user's browser.
    # the 'session' object keeps data between multiple requests
    session['some_var'] = "IRWA 2021 home"

    user_agent = request.headers.get('User-Agent')
    print("Raw user browser:", user_agent)

    user_ip = request.remote_addr
    agent = httpagentparser.detect(user_agent)

    print("Remote IP: {} - JSON user browser {}".format(user_ip, agent))

    print(session)


    return render_template('index.html', page_title="Welcome")


@app.route('/search', methods=['POST'])
def search_form_post():

    #out = datetime.now() #time when entered the results page
    
    #if enter < out:  #out is the time when we exited the visited page and went back to all results
    #    dwell_time = out-enter

    search_query = request.form['search-query']
    
    
    session['last_search_query'] = search_query

    search_id = analytics_data.save_query_terms(search_query)


    results = searchEngine.search(search_query)
    found_count = len(results)
    
    session['last_found_count'] = found_count
    print(session)

    return render_template('results.html', results_list=results[:20], page_title="Results", found_counter=found_count)


@app.route('/doc_details', methods=['GET'])
def doc_details():
    # getting request parameters:
    # user = request.args.get('user')
    
    #enter = datetime.now() #time when clicked the doc
    
    print("doc details session: ")
    print(session)
    res = session["some_var"]
    print("recovered var from session:", res)
    
    
    id = int(request.args.get('id'))
    title = request.args.get('title')
    
    
    clicked_doc_id = id
    #click = ClickedDoc(id, title, 1)
    #analytics_data.update(click)
    
    if clicked_doc_id in analytics_data.fact_clicks.keys():
        analytics_data.fact_clicks[clicked_doc_id] += 1
    else:
        analytics_data.fact_clicks[clicked_doc_id] = 1
    
    
    #fact_cl = analytics_data.fact_clicks
    #fact_cl_ret = click.update(fact_cl)
    #analytics_data.fact_clicks = fact_cl_ret
    #analytics_data.fact_clicks.append(Click(clicked_doc_id, "some desc"))

    #print("click in id={} - fact_clicks len: {}".format(clicked_doc_id, len(analytics_data.fact_clicks)))

    return render_template('doc_details.html', id = id, title = title)


@app.route('/stats', methods=['GET'])
def stats():
    """
    Show simple statistics example. ### Replace with dashboard ###
    :return:
    """
    ### Start replace with your code ###
    #docs = []
    #for clk in analytics_data.fact_clicks:
    #    docs.append((corpus[clk.doc_id]))
    docs = []
    for d_id in analytics_data.fact_clicks:
        c = analytics_data.fact_clicks[d_id] #counter
        print('***', c, d_id)

        for tweet in corpus:
            if d_id == int(tweet.id_json):
                print('yes', d_id)
        
        
                doc = ClickedDoc(doc_id = (tweet.id_json), description = tweet.title, counter = c)
                docs.append(doc)
            
            
    docs.sort(key=lambda doc: doc.counter, reverse=True) #rank clicked documents descendingly (by number of visits)
    
    
    numw_sq = analytics_data.query_length
    
    
    return render_template('stats.html', num_words_sq = numw_sq, clicks_data=docs)
    ### End replace with your code ###


@app.route('/dashboard', methods=['GET'])
def dashboard():
    """
    visited_docs = []
    print(analytics_data.fact_clicks.keys())
    
    for doc_id in analytics_data.fact_clicks.keys():
        d: Document = corpus[int(doc_id)]
        doc = ClickedDoc(doc_id, d.description, analytics_data.fact_clicks[doc_id])
        visited_docs.append(doc)
    
    # simulate sort by ranking
    visited_docs.sort(key=lambda doc: doc.counter, reverse=True)

    for doc in visited_docs: print(doc)
    return render_template('dashboard.html', visited_docs=visited_docs)
    """

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
    app.run(port="8088", host="0.0.0.0", threaded=False, debug=True)
