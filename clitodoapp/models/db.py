import os
import logging


from peewee import SqliteDatabase



LOG = logging.getLogger(__name__)

db = SqliteDatabase("db.db")
