# from flask_pymongo import PyMongo
# from flask import Flask
# import os

# app = Flask(__name__)


# class ConnectDb:
#     def init_db():
#         user = os.environ.get("MONGO_USER")
#         pw = os.environ.get("MONGO_PASSWORD")
#         mongodb_client = PyMongo(
#             app,
#             uri="mongodb+srv://{user}:{pw}@cluster0.afxa4.mongodb.net/myDb?retryWrites=true&w=majority",
#         )
