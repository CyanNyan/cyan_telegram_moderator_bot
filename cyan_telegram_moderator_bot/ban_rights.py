from telegram import ChatPermissions
import logging
from .update_db import connect_mongo, is_qualified

def ban_rights(update, context):
	"""Ban all rights except send text when first enter group"""

	logging.info("restricted")

	collection = connect_mongo()
	if is_qualified(update.message.from_user.id, collection): # returned user will have default privileges of the group
		return

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