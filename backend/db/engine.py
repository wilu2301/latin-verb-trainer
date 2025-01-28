import pymongo
from .. import settings

client = pymongo.MongoClient(settings.MONGO_URL)
db = client[settings.MONGO_DB]