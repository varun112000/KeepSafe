from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "Varun"

cluster = MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false")
db = cluster["Enrollment"]
User = db["User"]
WebPassword = db["WebPassword"]


from Application import routes