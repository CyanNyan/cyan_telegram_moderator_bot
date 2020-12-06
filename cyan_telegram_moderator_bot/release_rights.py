from telegram import ChatPermissions
import logging

def release_rights(update, context, user_id):
	"""When the user is qualified(see is_qualified), enable other user permissions

	The enabled permissions include:
	 'Send Media',
	 'Send Sticker & GIFs',
	 'Send Polls',
	 'Embed Links',
	 'Add User'

	"""
	
	logging.info("Releasing right")
	permissions = ChatPermissions(can_send_messages = True, can_send_media_messages = True, 
		can_send_polls = True, can_send_other_messages = True, can_add_web_page_previews = True,
		can_change_info = False, can_invite_users = True, can_pin_messages = False)

	context.bot.restrict_chat_member(update.message.chat_id, user_id, permissions)
	logging.info("Should be released")
