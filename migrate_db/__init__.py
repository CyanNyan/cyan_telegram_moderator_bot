from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
import os
from .versions import VERSIONS, VERSION_NAMES


def migrate(update, context):
    if len(context.args) <= 0:
        return
    logging.info("migrate started")
    version_name = context.args[0]
    if version_name in VERSION_NAMES:
        update.effective_chat.send_message('*** Migration in progress ***')
        version = VERSION_NAMES[version_name]
        message = VERSIONS[version](update, context)
        update.effective_chat.send_message(
            'Migration completed! ��\nNew version: v{} ({})\n{}'.format(version, version_name, message))


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

updater = Updater(token=os.environ['TOKEN'], use_context=True)
dispatcher = updater.dispatcher
migrate_handler = CommandHandler('migrate', migrate)
dispatcher.add_handler(migrate_handler)
