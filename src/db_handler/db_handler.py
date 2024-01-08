import pymongo

from logger import Log

log = Log("db_handler")

class DbHandler:
    def __init__(self, db_name, collection_name):
        log.debug(f"Initializing DBHandler for {db_name}.{collection_name}")
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        log.debug(f"DBHandler initialized")
    def get_collector_names(self):
        log.debug(f"Getting collector names")
        collector_names = self.collection.distinct("collectorName")
        log.info(f"Collector names: {collector_names}")
        return collector_names

    def get_collector_info(self, collector_name):
        log.debug(f"Getting collector info for {collector_name}")
        collector_info = self.collection.find_one({"collectorName": collector_name})
        log.info(f"Collector info: {collector_info}")
        return collector_info