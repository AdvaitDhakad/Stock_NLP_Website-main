from flask import Flask, request
from flask_restful import reqparse, Api, Resource
from flask_cors import CORS,cross_origin
from summarizer_sentiment import get_sentiment, tfidf_summarize
from finance_data import get_news_link
from historical_data import get_symbol

app = Flask(__name__)
api = CORS(app)
# https://www.kaggle.com/code/advaitdhakad/stock-market-prediction-using-cnn-lstm-d6af07/edit

parser = reqparse.RequestParser()
parser.add_argument('task')

@app.route('/api/backend/', methods=['GET', 'POST'])
def index():
    return 'THIS IS THE THE PYTHON SERVER FOR THE API AND MACHINE LEARNING '

@app.route('/api/', methods=['GET', 'POST'])
@cross_origin()
def predict():
    args = parser.parse_args()
    body = request.json
    body = dict(body)
    print(body["sentence"])
    try:
        sentiment = get_sentiment(body["sentence"])
        if len(body["sentence"].split()) > 100:
            summary = tfidf_summarize(body["sentence"])
        elif len(body["sentence"].split()) == 0:
            summary = "PLEASE ENTER A VALID SENTENCE"
            sentiment = "Error"
        else: 
            summary = body["sentence"]
    except ZeroDivisionError:
        summary = "PLEASE ENTER A VALID SENTENCE"
        sentiment = "Error"
    return {"summary": summary, "sentiment": sentiment}


@app.route('/api/finance/', methods=['GET', 'POST'])
@cross_origin()
def predict_finance():
    args = parser.parse_args()
    body = request.json
    body = dict(body)
    print(body["company"])
    try:
        news_links = get_news_link(body["company"])
    except Exception as e:
        news_links = "Error"
    return {"news_links": news_links}


@app.route('/api/model/', methods=['GET', 'POST'])
@cross_origin()
def model():
    args = parser.parse_args()
    body = request.json
    body = dict(body)
    print(body["company"])
    try:
        df = get_symbol(body["company"])
        return {"data":df.to_html()}    
    except Exception as e:
        print(e)
        return {"hehe":e}
  

if __name__ == '__main__':
    app.run(debug=True)