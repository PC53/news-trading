import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
import urllib.request
import pandas as pd
import json
import time
from datetime import date
import csv
from datetime import datetime, timedelta
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import yfinance as yf
from tickers import TICKERS

FLASK_SENTIMENT_API = "http://127.0.0.1:5000/insert_sentiments"

class stockSentiment:
    def __init__(self, ticker):
        self.ticker = ticker
        
    def get_articles_headlines(self):
        url = "https://finance.yahoo.com/quote/"+str(self.ticker)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news = soup.find('div',attrs={'id':'tabpanel-news'}).findAll('a')
        news = [i['title'] for i in news]
        return news  
    
    def get_article_headlines_yf(self):
        stock = yf.Ticker(self.ticker)
        return [s['title'] for s in stock.news]
            
    
    def parser(self):
        news_txt = []
        news = self.get_article_headlines_yf()
        for i in news:
            news_txt.append(str(i))
            break
        return news_txt
    
    #We define a DataFrame of headlines and we assess the sentiment for each
    def news_sent(self):
        headlines = self.parser()
        sia = SentimentIntensityAnalyzer()
        output = []
        for i in headlines:
            pol_score = sia.polarity_scores(i)
            output.append(pol_score)
        output = pd.json_normalize(output)
        df_output = pd.DataFrame(data=output)  
        return df_output
    
    #This method returns the aggregated sentiment value of the reference company:
    def get_averages(self):
        base_df = self.news_sent()
        averages = base_df.mean()
        avg_df = pd.DataFrame(data=averages).T
        return avg_df
    
    #Method to build the df of a company's aggregated sentiment:
    def sentiment(self):
        ticker = self.ticker
        sentiment = self.get_averages()
        #sentiment['Ticker']=ticker
        sentiment.insert(0,'Ticker',ticker)
        return sentiment

    #Method to build a df of all the companies in a specified list of tickers:
    def get_all_sentiments(tickers):        
        today = date.today()
        start = time.time()
        main = pd.DataFrame()
        for i in tickers:
            x = stockSentiment(i)
            y = x.sentiment()
            main = pd.concat([main,y],ignore_index=True)
            
        main['datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        end = time.time()
        print("Date:", today)
        print("Stocks analyzed: ", len(tickers))
        print("Execution time: ", end - start)
        return main
    
    def scrape_news():
        print(f"Starting getting news...")
        main = stockSentiment.get_all_sentiments(TICKERS)
        main.fillna(value=0, inplace=True)
        data_dict = main.to_dict(orient="records")
        
        response = requests.post(FLASK_SENTIMENT_API, json = data_dict)
                
        if response.status_code == 201:
            print("Inserted IDs:", response.json()["inserted_ids"])
            print(f"Data added to Database, Next Job scheduled on {datetime.today() + timedelta(1)} ")
        else:
            print("Failed to insert data.")
            print("Error:", response.json()["error"])

        return response
    
    
def schedule(hr = 9,min = 30):
    scheduler = BlockingScheduler()
    scheduler.add_job(stockSentiment.scrape_news, 'cron', hour = hr, minute = min) 
    scheduler.start()
    
if __name__ == '__main__':
    schedule(16,53)
