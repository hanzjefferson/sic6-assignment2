from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://rplmaalma6:rplmaalma6@sic-assignment.esiqb.mongodb.net/?retryWrites=true&w=majority&appName=sic-assignment")
db = client['assignment2']
collection = db['temperature']
