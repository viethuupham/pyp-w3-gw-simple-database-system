import os
from datetime import date

from simple_database.exceptions import ValidationError
from simple_database.config import BASE_DB_FILE_PATH


class Table(object):

    def __init__(self, db, name, columns=None):
        pass

    def insert(self, *args):
        pass

    def query(self, **kwargs):
        pass

    def all(self):
        pass

    def count(self):
        pass

    def describe(self):
        pass


class DataBase(object):
    def __init__(self, name):
        pass

    @classmethod
    def create(cls, name):
        pass

    def create_table(self, table_name, columns):
        pass

    def show_tables(self):
        pass


def create_database(db_name):
    """
    Creates a new DataBase object and returns the connection object
    to the brand new database.
    """
    DataBase.create(db_name)
    return connect_database(db_name)


def connect_database(db_name):
    """
    Connectes to an existing database, and returns the connection object.
    """
    return DataBase(name=db_name)
