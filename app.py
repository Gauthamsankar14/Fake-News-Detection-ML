from flask import Flask,render_template,jsonify, request
from newsapi import NewsApiClient
from predictionModel import PredictionModel
import pandas as pd
from random import randrange

app = Flask(__name__, static_folder="./public/static",
            template_folder="./public")


@app.route("/")
def home():
    api_key = "eb0aa70216a648f4a8f01c74fb9f07bf"
    
    newsapi = NewsApiClient(api_key=api_key)

    top_headlines = newsapi.get_top_headlines(sources = "bbc-news")
    all_articles = newsapi.get_everything(sources = "bbc-news")
    

    t_articles = top_headlines['articles']
    a_articles = all_articles['articles']
    
    
    news = []
    desc = []
    img = []
    p_date = []
    url = []

    for i in range (len(t_articles)):
        main_article = t_articles[i]

        news.append(main_article['title'])
        desc.append(main_article['description'])
        img.append(main_article['urlToImage'])
        p_date.append(main_article['publishedAt'])
        url.append(main_article['url'])

        contents = zip( news,desc,img,p_date,url)

    news_all = []
    desc_all = []
    img_all = []
    p_date_all = []   
    url_all = []

    for j in range(len(a_articles)): 
        main_all_articles = a_articles[j]   

        news_all.append(main_all_articles['title'])
        desc_all.append(main_all_articles['description'])
        img_all.append(main_all_articles['urlToImage'])
        p_date_all.append(main_all_articles['publishedAt'])
        url_all.append(main_article['url'])
        
        all = zip( news_all,desc_all,img_all,p_date_all,url_all)

    return render_template('home.html',contents=contents,all = all)

@app.route('/index')
def index():
     return render_template('index.html')
@app.route('/predict', methods=['POST'])
def predict():
    model = PredictionModel(request.json)
    return jsonify(model.predict())


@app.route('/random', methods=['GET'])
def random():
    data = pd.read_csv("data/fake_or_real_news_test.csv")
    index = randrange(0, len(data)-1, 1)
    return jsonify({'title': data.loc[index].title, 'text': data.loc[index].text})     



if __name__ == '__main__':
    app.run()

