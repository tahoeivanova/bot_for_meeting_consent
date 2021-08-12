import pprint
from pymongo import MongoClient
from credentials import mongo_link
# mongodb+srv://<username>:<password>@cluster0.osunc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority

# username = ''
# password = ''
# db_name = ''
# client = MongoClient('''mongodb://{username}:{password}@cluster0.twwbx.mongodb.net/{db_name}retryWrites=true&w=majority'''
#                      .format(username=username, password=password, db_name=db_name))


client = MongoClient(mongo_link)
# client = MongoClient('mongodb://{username}:{password}@cluster0.twwbx.mongodb.net/{db_name}?retryWrites=true&w=majority')

db = client.when_where_db

# when_where = db.when_where
#
# # users = db.users
# #
# import datetime
# personDocument = {
#   "name": { "first": "Alan", "last": "Turing" },
#   "birth": datetime.datetime(1912, 6, 23),
#   "death": datetime.datetime(1954, 6, 7),
#   "contribs": [ "Turing machine", "Turing test", "Turingery" ],
#   "views": 1250000
# }
#
# when_where.insert_one(personDocument)
# users.insert_one(personDocument)
# #
# obj = users.find_one({ "name.last": "Turing" })
#
# pprint.pprint(obj)

