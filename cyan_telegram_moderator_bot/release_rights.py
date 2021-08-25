import logging
from .permissions import RELEASED_PERMISSIONS
from telegram.constants import CHATMEMBER_CREATOR, CHATMEMBER_ADMINISTRATOR


def release_rights(bot, chat_id, user_id):
    """When the user is qualified(see is_qualified), enable other user permissions

    The enabled permissions include:
     'Send Media',
     'Send Sticker & GIFs',
     'Send Polls',
     'Embed Links',
     'Add User'

    """

    logging.info("Releasing right")
    chat_member = bot.get_chat_member(chat_id, user_id)
    if chat_member.status in {CHATMEMBER_CREATOR, CHATMEMBER_ADMINISTRATOR}:
        logging.info('Skip creator or administrator!')
        return

    bot.restrict_chat_member(chat_id, user_id, RELEASED_PERMISSIONS)
    logging.info("Should be released")
