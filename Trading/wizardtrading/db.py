from wizardtrading.loggingUtils import LogFactory
import pymongo
import os

logger = LogFactory.getLogger(__name__)

DB_CLIENT_CONNECTION_URL = os.getenv('MONGODB_DB_URL')
DB_NAME = os.getenv('DBNAME')
DB_COLLECTION_NAME = os.getenv('COLLECTION')

# Singleton Database class
class Database():

    db_client_ = None
    db_instance_ = None
    db_collection_instance_ = None

    def __init__(self):
        if Database.db_client_ is None:
            Database.db_client_ = pymongo.MongoClient(DB_CLIENT_CONNECTION_URL)
            dblist = Database.db_client_.list_database_names()
            if DB_NAME in dblist:
                logger.info(f"{DB_NAME} exists")
            Database.db_instance_ = Database.db_client_[DB_NAME]
            collectionslist = Database.db_instance_.list_collection_names()
            if DB_COLLECTION_NAME in collectionslist:
                logger.info(f"{DB_COLLECTION_NAME} exists")
            Database.db_collection_instance_ = Database.db_instance_[DB_COLLECTION_NAME]

    def insertRecord(data):
        status = Database.db_collection_instance_.insert_one(data)