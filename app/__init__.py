from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
mongo = MongoClient(app.config['MONGO_URI'], server_api=ServerApi('1'))

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

from app import routes
