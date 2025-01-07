from peewee import *
from playhouse.sqlite_ext import JSONField
import os


path = os.path.dirname(os.path.abspath(__file__))
dbpath = os.path.join(path, '../../../../database.sqlite')

db = SqliteDatabase(dbpath)

class Home(Model):
    class Meta:
        database = db
        table_name = 'homes'
    id = AutoField()
    name = CharField()
    council = CharField()
    council_data = JSONField()
    active = BooleanField()

    @classmethod
    def get_active(cls):
        return cls.get_or_none(cls.active == True)


class Bin(Model):
    class Meta:
        database = db
        table_name = 'bins'

    id = AutoField()
    council_name = CharField()
    name = CharField()
    position = IntegerField()
    home_id = ForeignKeyField(Home, backref='bins')