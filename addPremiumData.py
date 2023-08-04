import pandas as pd
from flask import Flask
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
mongo = MongoClient(app.config['MONGO_URI'], server_api=ServerApi('1'))

db = mongo["premium"]

df = pd.read_excel("seed_data/assignment_raw_rate.xlsx")
seedData = []

for index, row in df.iterrows():
    rowJson = {}
    rowJson['city_tier'] = row['TierID']
    rowJson['product_code'] = row['ProductCode']
    rowJson['plan_code'] = row['PlanCode']
    rowJson['plan_name'] = row['PlanName']
    rowJson['age'] = row['Age']
    rowJson['insure_pattern'] = row['InsuredPattern']
    rowJson['sum_insured'] = row['SumInsured']
    rowJson['tenure'] = row['Tenure']
    rowJson['rate'] = row['Rate']
    seedData.append(rowJson)

db.premiumRate.insert_many(documents=seedData)
