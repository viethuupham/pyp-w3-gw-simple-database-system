import os
import json
from datetime import date

from simple_database.exceptions import ValidationError
from simple_database.config import BASE_DB_FILE_PATH


class Row(object):
    def __init__(self, row):
        for key, value in row.items():
            setattr(self, key, value)

class Table(object):

    def __init__(self, db, name, columns=None):
        self.db = db
        self.name = name

        self.table_filepath = os.path.join(BASE_DB_FILE_PATH, self.db.name,
                                           '{}.json'.format(self.name))

        # In case the table JSON file doesn't exist already, you must
        # initialize it as an empty table, with this JSON structure:
        # {'columns': columns, 'rows': []}
        
        if not os.path.exists(self.table_filepath):
            with open(self.table_filepath, 'w') as f:
                table = {'columns': columns, 'rows': []}
                f.write(json.dumps(table))
                
        self.columns = columns or self._read_columns()

    def _read_columns(self):
        # Read the columns configuration from the table's JSON file
        # and return it.
        with open(self.table_filepath, 'r') as f:
            data = json.load(f)
            return data['columns']
            
    def insert(self, *args):
        # Validate that the provided row data is correct according to the
        # columns configuration.
        # If there's any error, raise ValidationError exception.
        # Otherwise, serialize the row as a string, and write to to the
        # table's JSON file.
        
        #check if data is correct format and type
        if len(self.columns) != len(args):
            raise ValidationError('Invalid amount of field')
        
        to_insert = {}
        for col_type, insert_value in zip(self.columns, args):
            if type(insert_value).__name__ == col_type['type']:
                to_insert[col_type['name']] = insert_value
            else:
                raise ValidationError('Invalid type of field "{}": Given "{}", expected "{}"'.format(
                                    col_type['name'], type(insert_value).__name__, col_type['type']))
        
        with open(self.table_filepath, 'r+') as f:
            data = json.load(f)
            data['rows'].append(to_insert)
            f.seek(0)
            f.write(json.dumps(data, cls=DateTimeEncoder))
                

    def query(self, **kwargs):
        # Read from the table's JSON file all the rows in the current table
        # and return only the ones that match with provided arguments.
        # We would recomment to  use the `yield` statement, so the resulting
        # iterable object is a generator.

        # IMPORTANT: Each of the rows returned in each loop of the generator
        # must be an instance of the `Row` class, which contains all columns
        # as attributes of the object.
        
        with open(self.table_filepath, 'r') as f:
            data = json.load(f)
            for row in data['rows']:
                for k, v in kwargs.items():
                    if v == row[k]:
                        yield Row(row)
            
    def all(self):
        # Similar to the `query` method, but simply returning all rows in
        # the table.
        # Again, each element must be an instance of the `Row` class, with
        # the proper dynamic attributes.
        
        with open(self.table_filepath, 'r') as f:
            data = json.load(f)
            for row in data['rows']:
                yield Row(row)
            
    def count(self):
        # Read the JSON file and return the counter of rows in the table
        with open(self.table_filepath, 'r') as f:
            data = json.load(f)
            return len(data['rows'])

    def describe(self):
        # Read the columns configuration from the JSON file, and return it.
        return self.columns


class DataBase(object):
    def __init__(self, name):
        self.name = name
        self.db_filepath = os.path.join(BASE_DB_FILE_PATH, self.name)
        self.tables = self._read_tables()

    @classmethod
    def create(cls, name):
        db_filepath = os.path.join(BASE_DB_FILE_PATH, name)
        # if the db directory already exists, raise ValidationError
        # otherwise, create the proper db directory
        
        if not os.path.exists(db_filepath):
            os.makedirs(db_filepath)
        else:
            raise ValidationError('Database with name "{}" already exists.'.format(name))

        
    def _read_tables(self):
        # Gather the list of tables in the db directory looking for all files
        # with .json extension.
        # For each of them, instatiate an object of the class `Table` and
        # dynamically assign it to the current `DataBase` object.
        # Finally return the list of table names.
        # Hint: You can use `os.listdir(self.db_filepath)` to loop through
        #       all files in the db directory
        table_list = []
        for table in os.listdir(self.db_filepath):
            if table.endswith('.json'):
                table = table.replace('.json','') #remove the .json from the end
                setattr(self, table, Table(self,table))
                table_list.append(table)
            
        return table_list
                

    def create_table(self, table_name, columns):
        # Check if a table already exists with given name. If so, raise
        # ValidationError exception.
        # Otherwise, crete an instance of the `Table` class and assign
        # it to the current db object.
        # Make sure to also append it to `self.tables`
        
        #__init__(self, db, name, columns=None):
        
        if not os.path.isfile(os.path.join(self.db_filepath,table_name)):
            new_table = Table(self, table_name, columns)
            setattr(self, table_name, new_table)
            self.tables.append(table_name)
        else:
            raise ValidationError("Table already exists.")
        
            
    def show_tables(self):
        # Return the curren list of tables.
        return self.tables


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


#Allow date to be serializable
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)