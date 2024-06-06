from flask import Flask, request, jsonify
from pymongo import MongoClient
import pandas as pd
import json
from datetime import datetime, time
import urllib.parse
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MongoDB configuration
MONGODB_URI = "mongodb://localhost:27017/"
DB_NAME = "newstradingDB"

# Function to add DataFrame to MongoDB
def add_dataframe_to_mongodb(df, db_name, collection_name, mongodb_uri=MONGODB_URI):
    client = MongoClient(mongodb_uri)
    db = client[db_name]
    collection = db[collection_name]
    data_dict = df.to_dict(orient="records")
    result = collection.insert_many(data_dict)
    client.close()
    return result

# Endpoint to insert data into MongoDB
@app.route('/insert_sentiments', methods=['POST'])
def insert_sentiments():
    try:
        data = request.json
        df = pd.DataFrame(data)
        
        if 'datetime' in df.columns:
            df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S')
        
        result = add_dataframe_to_mongodb(df, DB_NAME, 'sentiments')
        return jsonify({"inserted_ids": str(result.inserted_ids)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to retrieve sentiments from MongoDB
@app.route('/get_sentiments', methods=['GET'])
def get_sentiments():
    try:
        client = MongoClient(MONGODB_URI)
        db = client[DB_NAME]
        collection = db['sentiments']
        
        #get the last date in the database
        last_date = collection.find_one(sort=[("datetime", -1)])['datetime']
        start_of_day = datetime.combine(last_date, time.min)       
        
        # Query to fetch records after the specified time
        documents = list(collection.find({"datetime": {"$gt": start_of_day}}, {"_id": 0}))  # Exclude the _id field
        client.close()
        
        return jsonify(documents), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
