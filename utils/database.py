from pymongo import MongoClient
import os

client = MongoClient(
    f"mongodb+srv://PonixBotDiscloud:{os.getenv('PASS')}@cluster0.w3eys.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = client.database
