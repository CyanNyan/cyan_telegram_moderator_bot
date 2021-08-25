import logging
from .update_db import is_qualified
from .db import collection_group
from .permissions import RESTRICTED_PERMISSIONS, RELEASED_PERMISSIONS


def ban_rights(update, context):
    """Ban all rights except send text when first enter group"""
    group_info = collection_group().find_one({'chat_id': update.effective_chat.id})

    for new_member in update.message.new_chat_members:
        # receive info from new member
        # set the right in permissions
        if is_qualified(update.effective_chat.id, new_member.id):
            logging.info('{} is already qualified!'.format(new_member.first_name))
            context.bot.restrict_chat_member(
                update.message.chat_id, new_member.id, RELEASED_PERMISSIONS)
        else:
            logging.info('{} is restricted!'.format(new_member.first_name))
            context.bot.restrict_chat_member(
                update.message.chat_id, new_member.id, RESTRICTED_PERMISSIONS)

        if group_info:
            welcome_text = group_info['welcome_message']
            update.message.reply_text(welcome_text.format(
                first_name=new_member.first_name,
                last_name=new_member.last_name
            ))
