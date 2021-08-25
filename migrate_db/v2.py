from cyan_telegram_moderator_bot.db import collection_user, collection_counts, init_counts


def v2migrate(update, context):
    chat_id = update.effective_chat.id
    users = collection_user().find()
    total_users_count = 0
    migrated_users_count = 0
    for user in users:
        total_users_count += 1
        counts = collection_counts().find_one({'chat_id': chat_id, 'user_id': user['user_id']})
        if counts:
            if user['count'] <= 0:
                continue
            collection_counts().update_one({
                'chat_id': chat_id,
                'user_id': user['user_id']
            }, {'$inc': {'count': user['count']}})
            collection_user().update_one({
                'user_id': user['user_id']
            }, {'$set': {'count': 0}})
        else:
            init_counts(chat_id, user['user_id'], user['count'], user['is_qualified'])
        migrated_users_count += 1

    return 'Total user: {}, migrated user: {}'.format(total_users_count, migrated_users_count)
