from telegram.ext import Filters, Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram import ChatPermissions
import logging, os

def start(update, context):
	logging.info("start detected")
	context.bot.send_message(chat_id=update.effective_chat.id, text="Cyan is cute!")

def ban_rights(update, context):
	"""Ban all rights except send text when first enter group"""
	
	logging.info("restricted")
	permissions = ChatPermissions(can_send_messages = True, can_send_media_messages = False, 
		can_send_polls = False, can_send_other_messages = False, can_add_web_page_previews = False,
		can_change_info = False, can_invite_users = False, can_pin_messages = False)

	for new_member in update.message.new_chat_members:
		# receive info from new member
		callback_id = str(new_member.id)
		# set the right in permissions

		logging.info("restricted")
		context.bot.restrict_chat_member(update.message.chat_id, new_member.id, permissions)

	update.message.reply_text(
		'Hello, ' +
		new_member.first_name +
		'. Welcome to the group! Please stay active so you can send sticker and media later XD'
		)


def release_rights(update, context):
	"""When the user is qualified(see is_qualified), enable other user permissions

	The enabled permissions include:
	 'Send Media',
	 'Send Sticker & GIFs',
	 'Send Polls',
	 'Embed Links',
	 'Add User'

	"""

	pass

def is_qualified(user_id):
	"""Check if the member has reached the required number of sent messages
	
	return True or False

	"""
	pass


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=os.environ['TOKEN'], use_context=True)
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start)

logging.info("start")

dispatcher.add_handler(start_handler)
dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, ban_rights))

updater.start_polling()
