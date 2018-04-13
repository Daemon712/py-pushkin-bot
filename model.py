import os
import re
from datetime import datetime

from pony.orm import Database, Required, Optional, PrimaryKey, db_session, select, count

databaseUrl = os.environ.get("DATABASE_URL")
matcher = re.search('postgres://(?P<user>.+):(?P<password>.+)@(?P<host>.+):(?P<port>.+)/(?P<database>.+)', databaseUrl)

db = Database()
db.bind(provider='postgres',
        user=matcher.group('user'),
        password=matcher.group('password'),
        host=matcher.group('host'),
        port=matcher.group('port'),
        database=matcher.group('database'))


class MessageEntity(db.Entity):
    _table_ = 'message_entity'
    chat_id = Required(int)
    message_id = Required(int)
    user_id = Required(int)
    date = Optional(datetime)
    text = Optional(str)
    # word_usages = Set(lambda: WordUsage, reverse='message')
    PrimaryKey(chat_id, message_id)


class GlobalDict(db.Entity):
    _table_ = 'global_dict'
    speech_part = Required(int)
    word = Required(str)
    rate = Required(float)
    PrimaryKey(speech_part, word)


class WordUsage(db.Entity):
    _table_ = 'word_usage'
    index = Required(int)
    chat_id = Required(int)
    message_id = Required(int)
    # message = Required(MessageEntity, reverse='word_usages')
    speech_part = Required(int)
    word = Required(str)
    PrimaryKey(chat_id, message_id, index)


db.generate_mapping(create_tables=False)


if __name__ == '__main__':
    with db_session:
        print(select(count(gd) for gd in WordUsage)[:])
        print(select(count(gd) for gd in MessageEntity)[:])
        print(select(count(gd) for gd in GlobalDict)[:])

