from telegram.ext import Filters, Updater
from telegram.ext import CommandHandler, MessageHandler
import logging, os
from .ban_rights import ban_rights
from .release_rights import release_rights
from .update_db import update_db

def start(update, context):
	logging.info("start detected")
	context.bot.send_message(chat_id=update.effective_chat.id, text="Cyan is cute!")

def is_qualified(user_id):
	"""Check if the member has reached the required number of sent messages
	
	return True or False

	"""
	pass

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info("start")

updater = Updater(token=os.environ['TOKEN'], use_context=True)
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start)

# send start message
dispatcher.add_handler(start_handler)

# ban the rights except 'Send Text' for new useres
dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, ban_rights))

# update message count, including stickers
dispatcher.add_handler(MessageHandler(Filters.update.message & Filters.text, update_db))