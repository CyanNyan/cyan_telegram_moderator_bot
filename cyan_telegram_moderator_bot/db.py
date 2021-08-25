from pymongo import MongoClient
from os import environ


def connect_mongo():
    client = MongoClient(environ["DATABASE_URL"])
    db = client[environ['DATABASE_NAME']]
    return db


def collection_user():
    db = connect_mongo()
    return db['collection']


def collection_counts():
    db = connect_mongo()
    return db['message_counts']


def collection_group():
    db = connect_mongo()
    return db['groups']


def init_user(userid, username, first_name, last_name):
    post = {
        'user_id': userid,
        'user_name': username,
        'first_name': first_name,
        'last_name': last_name,
        'count': 0,
        'is_qualified': False
    }
    collection_user().insert_one(post)


def init_counts(chat_id, user_id, init_count=0, is_qualified=False):
    count = {
        'chat_id': chat_id,
        'user_id': user_id,
        'is_qualified': is_qualified,
        'count': init_count
    }
    collection_counts().insert_one(count)


def init_group(chat_id, title=None):
    group = {
        'chat_id': chat_id,
        'title': title,
        'message_count': '60',
        'welcome_message': 'Hello, {first_name}. Welcome to the group! Please stay active so you can send sticker and media later XD',
        'echo': 'Cyan is cute!',
        'meow': '喵喵喵？'
    }
    collection_group().insert_one(group)
