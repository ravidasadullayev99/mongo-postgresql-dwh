from pymongo import MongoClient

MONGO_URI= 'mongodb://root:example@localhost:27017/?authSource=admin'

client = MongoClient(MONGO_URI)

db=client['source_db']
customers= db['customers']

for customer in customers.find():
    print(customer)