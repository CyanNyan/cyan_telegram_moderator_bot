#!/bin/sh
export TOKEN=
export DATABASE_URL=
export DATABASE_NAME=database
export MESSAGE_COUNT=3

python3 -m cyan_telegram_moderator_bot
# python3 -m migrate_db
