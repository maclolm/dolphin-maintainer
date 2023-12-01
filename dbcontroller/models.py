from datetime import datetime
from peewee import SqliteDatabase, Model, CharField, IntegerField, DateTimeField

DEFAULT_DB_FILE = 'database.db'
db = SqliteDatabase(DEFAULT_DB_FILE)

SUB_STATUS = (
    (2, 'active'),
    (1, 'soon_expired'),
    (-1, 'expired')
)


class Subscriber(Model):
    username = CharField(null=False)
    tg_id = IntegerField(null=False, unique=True)
    creation_datetime = DateTimeField(default=datetime.now)
    status = IntegerField(default=0, choices=SUB_STATUS)
    sub_days_count = IntegerField(default=0)

    class Meta:
        database = db
        db_table = 'subscribers'


class Owner(Model):
    username = CharField(null=False)
    tg_id = IntegerField(null=False, unique=True)

    class Meta:
        database = db
        db_table = 'owners'
