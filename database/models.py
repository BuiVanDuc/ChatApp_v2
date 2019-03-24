import datetime
import json
import os

from peewee import *
from peewee_migrate import Migrator

from settings import BASE_DIR

LIST_AUGI_GENDER = {
    "male": 0,
    "female": 1,
    "gay": 2,
    "lesbian": 3,
    "other": 4
}

LIST_AUGI_GENDER_VAL = [
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
]

LIST_MESSAGE_STATE = {
    "unread": 0,
    "read": 1
}

LIST_MESSAGE_STATE_VAL = [
    (0, 0),
    (1, 1)
]

chat_app_db = SqliteDatabase(os.path.join(BASE_DIR, 'database', 'chat_app.db'), pragmas={'journal_mode': 'wal'})

migrator = Migrator(chat_app_db)


class BaseModel(Model):
    """A base model that will use our Sqlite database."""

    class Meta:
        database = chat_app_db


class ListField(TextField):
    def db_value(self, list_items):
        return ';'.join(json.dumps(item) for item in list_items)

    def python_value(self, data):
        list_items = []
        if data and len(data) > 0:
            list_temp = data.split(';')
            for item in list_temp:
                item = json.loads(item)
                list_items.append(item)
        return list_items


@migrator.create_table
class ChatAppUser(BaseModel):
    username = CharField(max_length=255)
    password = CharField(max_length=128)
    fullname = CharField(max_length=255)
    email = CharField(max_length=255, unique=True)
    birthday = DateField()
    address = CharField(max_length=255)
    sex = IntegerField(default=LIST_AUGI_GENDER.get("male"), choices=LIST_AUGI_GENDER_VAL)

    class Meta:
        db_table = 'chat_app_user'


@migrator.create_table
class ChatAppMessage(BaseModel):
    sender = ForeignKeyField(ChatAppUser)
    receiver = ForeignKeyField(ChatAppUser)
    message = TextField()
    is_read = SmallIntegerField(default=LIST_MESSAGE_STATE.get("unread"), choices=LIST_MESSAGE_STATE_VAL)
    sent_date = DateTimeField(default=datetime.datetime.utcnow())
    read_date = DateTimeField(default=None, null=True)

    class Meta:
        db_table = 'chat_app_message'


@migrator.create_table
class ChatAppFriend(BaseModel):
    user = ForeignKeyField(ChatAppUser)
    friend = ForeignKeyField(ChatAppUser)
    created_at = DateTimeField(default=datetime.datetime.utcnow())

    class Meta:
        db_table = 'chat_app_friend'


@migrator.create_table
class ChatAppBlockUser(BaseModel):
    blocker = ForeignKeyField(ChatAppUser)
    user = ForeignKeyField(ChatAppUser)
    created_at = DateTimeField(default=datetime.datetime.utcnow())

    class Meta:
        db_table = 'chat_app_blocking_user'


def convert_sex_number_to_name(sex_number):
    for key, value in LIST_AUGI_GENDER.items():
        if value == sex_number:
            return key

