import logging
import os
from .release_rights import release_rights
from .db import collection_group, collection_counts, collection_user, init_counts, init_group, init_user


def is_qualified(chat_id, user_id):
    group_info = collection_group().find_one({'chat_id': chat_id})
    if group_info:
        min_message_count = int(group_info.get('message_count'))
    else:
        min_message_count = int(os.environ['MESSAGE_COUNT'])
    if collection_counts().count_documents({
        'chat_id': chat_id,
        'user_id': user_id,
        'count': {"$gte": min_message_count}
    }, limit=1):
        return True


def update_db(update, context):
    """update message count
    stickers are counted as well"""
    user_id = update.effective_user.id
    user_name = update.effective_user.username
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    chat_id = update.effective_chat.id
    title = update.effective_chat.title

    logging.info(
        "New messsage: group {}, username {}, id {} ".format(
            chat_id, user_name, user_id))

    groups = collection_group()
    if groups.count_documents({'chat_id': chat_id}, limit=1) == 0:
        init_group(chat_id)
        logging.info(
            "New group: title {}, id {}".format(title, chat_id))

    collection = collection_user()
    if collection.count_documents({'user_id': user_id}, limit=1) == 0:
        # if user doesn't exist, add it to database and set message count to 1
        init_user(user_id, user_name, first_name, last_name)
        logging.info(
            "First message: group {}, username {}, id {}".format(
                chat_id, user_name, user_id))

    counts = collection_counts()
    if counts.count_documents(
            {'chat_id': chat_id, 'user_id': user_id}, limit=1) == 0:
        init_counts(chat_id, user_id, 1)
    else:  # if user exists, increment message count
        counts.update_one(
            {'chat_id': chat_id, 'user_id': user_id}, {'$inc': {'count': 1}})
        message_count = counts.find_one(
            {'chat_id': chat_id, 'user_id': user_id})['count']
        logging.info(
            'Increment message count: group {}, by {}, id {}, current message count is {}'.format(
                chat_id,
                user_name,
                user_id,
                message_count))

    # check, if qualifies, release rights
    if is_qualified(chat_id, user_id) and not counts.find_one({
        'chat_id': chat_id,
        'user_id': user_id
    })['is_qualified']:
        release_rights(context.bot, chat_id, user_id)
        counts.update_one({'chat_id': chat_id, 'user_id': user_id},
                          {"$set": {'is_qualified': True}})
        logging.info(
            "Lock released: group {} username {}, id {}".format(
                chat_id, user_name, user_id))
