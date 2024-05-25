# scraper/scraper.py

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler

def scrape_news():
    client = MongoClient('mongodb://mongo:27017/')
    db = client['mytradingapp']
    news_collection = db.news

    # Example scraping logic
    url = 'https://example.com/news'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_list = soup.find_all('p')

    for news in news_list:
        news_collection.insert_one({"news_text": news.text})
    print("News data scraped and stored.")
    client.close()

scheduler = BlockingScheduler()
scheduler.add_job(scrape_news, 'cron', hour=5, minute=30)  # Customize time as needed
scheduler.start()
