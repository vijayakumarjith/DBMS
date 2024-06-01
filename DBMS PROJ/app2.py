from flask import Flask, render_template, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client.stark_news
news_collection = db.newsapp

@app.route('/', methods=['GET', 'POST'])
def index():
    articles = None
    date_str = None
    if request.method == 'POST':
        date_str = request.form.get('date')
        if not date_str:
            return render_template('index.html', error="Please provide a date in the format YYYY-MM-DD")
        
        try:
            query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return render_template('index.html', error="Invalid date format. Please use YYYY-MM-DD")

        # Query the collection for articles matching the date
        articles = news_collection.find({"date": str(query_date)})
        # Convert articles to a list
        articles = list(articles)
    
    return render_template('index.html', articles=articles, date=date_str)

if __name__ == '__main__':
    app.run(debug=True)
