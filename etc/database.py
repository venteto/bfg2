import peewee
from datetime import datetime

from etc.config import BFG_ENV


if BFG_ENV == 'DEV':
    db = peewee.SqliteDatabase('data/other/dev.db')
else:
    db = peewee.SqliteDatabase('data/live/test.db')
    # db = peewee.SqliteDatabase('data/live/prod.db')

db_version = 2

class BaseModel(peewee.Model):
    class Meta:
        database = db

class SubscriptionState(BaseModel):
    service = peewee.CharField(unique=True)
    cursor = peewee.IntegerField()


class DbMetadata(BaseModel):
    version = peewee.IntegerField()

# ------------------------------------------------

class Post(BaseModel):
    feed = peewee.CharField()
    text = peewee.CharField()
    acct = peewee.CharField()
    # auth_did = peewee.CharField(null=True, default=None)
    # existing fields:
    uri = peewee.CharField(index=True)
    cid = peewee.CharField()
    reply_parent = peewee.CharField(null=True, default=None)
    reply_root = peewee.CharField(null=True, default=None)
    indexed_at = peewee.DateTimeField(default=datetime.utcnow)

# ------------------------------------------------

if db.is_closed():
    db.connect()
    db.create_tables([SubscriptionState, DbMetadata, Post])

    # DB migration

    current_version = 1
    if DbMetadata.select().count() != 0:
        current_version = DbMetadata.select().first().version

    if current_version != db_version:
        with db.atomic():
            # V2
            # Drop cursors stored from the old bsky.social PDS
            if current_version == 1:
                SubscriptionState.delete().execute()

            # Update version in DB
            if DbMetadata.select().count() == 0:
                DbMetadata.insert({DbMetadata.version: db_version}).execute()
            else:
                DbMetadata.update({DbMetadata.version: db_version}).execute()
