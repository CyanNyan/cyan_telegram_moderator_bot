import pymongo
import logging
import os
from .release_rights import release_rights
from pymongo import MongoClient

def connect_mongo():
    client = MongoClient(os.environ["DATABASE_URL"])
    db = client.database
    collection = db.collection

    return collection

def init_user(userid, username, first_name, last_name, collection):
    post = {
        "user_id": userid,
        "user_name":username,
        "first_name": first_name,
        "last_name": last_name,
        'count': 0,
        "is_qualified": False
    }

    collection.insert_one(post)

def is_qualified(user_id, collection):
    if collection.count_documents({'user_id': user_id, 'count': {"$gte": 3}}, limit = 1):
        return True




def update_db(update, context):
    """update message count 
    stickers are counted as well"""
    user_id = update.message.from_user.id
    user_name = update.message.from_user.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name

    logging.info("New messsage by {}, id {} ".format(user_name, user_id))

    collection = connect_mongo()
    if collection.count_documents({'user_id': user_id }, limit = 1) == 0:
    # if user doesn't exist, add it to database and set message count to 1

        init_user(user_id, user_name, first_name, last_name, collection)
        logging.info("First message by {}, id {} stored".format(user_name, user_id))

    else: # if user exists, increment message count
        result = collection.update_one({'user_id': user_id}, {'$inc': {'count': 1}})
        message_count = collection.find_one({'user_id': user_id})['count']
        logging.info("Another message by {}, id {}, current message count is {}".format(user_name, user_id, message_count))


    # check, if qualifies, release rights
    if is_qualified(user_id, collection) and collection.find_one({'user_id': user_id})['is_qualified'] == False:
        release_rights(update, context, user_id)
        result = collection.update_one({'user_id': user_id}, { "$set": {'is_qualified': True}})
        logging.info("Lock released for {}, id {} ".format(user_name, user_id))



