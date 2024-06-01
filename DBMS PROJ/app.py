from flask import Flask, render_template, jsonify, request
import requests
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client.stark_news
news_collection = db.newsapp

def fetch_news(api_key, country='us', category=None):
    if category:
        url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={api_key}"
    else:
        url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}"
    
    response = requests.get(url)
    news_data = response.json()
    
    if 'articles' in news_data:
        articles = news_data['articles']
        # Save articles to MongoDB with today's date
        for article in articles:
            article['country'] = country
            article['category'] = category
            article['date'] = datetime.today().strftime('%Y-%m-%d')
            news_collection.update_one(
                {'title': article['title'], 'date': article['date']},
                {'$set': article},
                upsert=True
            )
        return articles
    else:
        print(f"Error fetching news: {news_data}")
        return []

api_key = '3c2dc110a037439ab3eb00f313a9cd8e'

@app.route('/')
def home():
    country = request.args.get('country', 'us')
    category = request.args.get('category')
    news_articles = fetch_news(api_key, country, category)
    return render_template('ig.html', articles=news_articles, country=country, category=category)

@app.route('/article')
def article():
    title = request.args.get('title')
    image_url = request.args.get('image')
    description = request.args.get('description')
    content = request.args.get('content')
    return render_template('article.html', title=title, image_url=image_url, description=description, content=content)

@app.route('/api/news')
def api_news():
    country = request.args.get('country', 'us')
    category = request.args.get('category')
    news_articles = fetch_news(api_key, country, category)
    return jsonify(news_articles)

if __name__ == '__main__':
    app.run(debug=True)
