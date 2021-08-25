from telegram.ext import Filters, Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram.constants import CHATMEMBER_CREATOR, CHATMEMBER_ADMINISTRATOR
import logging
import os
from random import randint
from .ban_rights import ban_rights
from .update_db import update_db
from .db import collection_group


def echo(update, context):
    logging.info("echo detected")
    group_info = collection_group().find_one({'chat_id': update.effective_chat.id})
    if group_info:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=group_info['echo'])


def meow(update, context):
    logging.info("meow detected")
    group_info = collection_group().find_one({'chat_id': update.effective_chat.id})
    if group_info:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=group_info['meow'])


def roll(update, context):
    logging.info("roll detected")
    limit = 100
    if len(context.args) > 0:
        try:
            limit = int(context.args[0])
        except ValueError:
            logging.info('User give an invalid number')
    if limit >= 1:
        result = randint(1, limit)
        update.effective_chat.send_message(result)


set_types = {
    'welcome': 'welcome_message',
    'echo': 'echo',
    'meow': 'meow',
    'message_count': 'message_count'
}


def set_message(update, context):
    logging.info('set message detected!')
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    chat_member = context.bot.get_chat_member(chat_id, user_id)
    if chat_member.status not in {CHATMEMBER_CREATOR, CHATMEMBER_ADMINISTRATOR}:
        logging.info('no permission to set message!')
        return

    group_info = collection_group().find_one({'chat_id': chat_id})
    if group_info and len(context.args) >= 2:
        set_type = context.args[0]
        set_content = ' '.join(context.args[1:])
        if set_type in set_types:
            collection_group().update_one({'chat_id': chat_id}, {'$set': {set_types[set_type]: set_content}})
            context.bot.send_message(
                chat_id=chat_id,
                text='Message updated for {}.'.format(set_type))


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logging.info("echo")
logging.info("meow")

updater = Updater(token=os.environ['TOKEN'], use_context=True)
dispatcher = updater.dispatcher
echo_handler = CommandHandler('echo', echo)
meow_handler = CommandHandler('meow', meow)
roll_handler = CommandHandler('roll', roll)
set_message_handler = CommandHandler('set', set_message)

# send start message
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(meow_handler)
dispatcher.add_handler(roll_handler)
dispatcher.add_handler(set_message_handler)

# ban the rights except 'Send Text' for new useres
dispatcher.add_handler(
    MessageHandler(
        Filters.chat_type.supergroup & Filters.status_update.new_chat_members,
        ban_rights))

# update message count, including stickers
dispatcher.add_handler(
    MessageHandler(
        Filters.chat_type.supergroup & Filters.update.message & Filters.text,
        update_db), group=1)
