from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
import pandas as pd

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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

mongo.db.premiumRate.insert_many(documents=seedData)
from app import routes
