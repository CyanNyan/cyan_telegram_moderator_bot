from telegram.ext import Filters, Updater
from telegram.ext import CommandHandler, MessageHandler
import logging, os
from .ban_rights import ban_rights
from .release_rights import release_rights
from .update_db import update_db

def echo(update, context):
	logging.info("echo detected")
	context.bot.send_message(chat_id=update.effective_chat.id, text="Cyan is cute!")

def meow(update, context):
        logging.info("meow detected")
        context.bot.send_message(chat_id=update.effective_chat.id, text="喵喵喵?")

def is_qualified(user_id):
	"""Check if the member has reached the required number of sent messages
	
	return True or False

	"""
	pass

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info("echo")
logging.info("meow")

updater = Updater(token=os.environ['TOKEN'], use_context=True)
dispatcher = updater.dispatcher
echo_handler = CommandHandler('echo', echo)
meow_handler = CommandHandler('meow', meow)

# send start message
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(meow_handler)

# ban the rights except 'Send Text' for new useres
dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, ban_rights))

# update message count, including stickers
dispatcher.add_handler(MessageHandler(Filters.update.message & Filters.text, update_db))
