# Hint 1

A main part of this project is file handling. The goal is that you get familiar with the Python interface to handle text files.

In this particular project we will be using JSON files. That's why we will need to make sure that every time we write something to the JSON files, it keeps respecting a JSON valid structure.

For that, we will use the built-in `json` library, as we will explain in a minute.

## Opening a file

Python offers s simple `open()` built-in function ([read more here](https://docs.python.org/2/library/functions.html#open)) that we can use to interact with files in the file system.

There're a few different ways of opening a file, mainly depending of what you want to do with it: reading, writing, appending content to the current file, etc.

The overall interface would be like this:

```python
file_object = open('/path/to/your/file', 'r')
# do something
file_object.close()
```

It's always important to close the connection to the file once we are done working with it. But, what happen if some error occurs in between we open and close the file, that blows the execution of the program and the `.close()` function is never called? Well, the file connection will remain opened, and that's never good.

For that, it's a very good convention to always use context managers to handle file openings, like this:

```python
with open('/path/to/your/file', 'r') as file_object:
    # do something
```

As the Python `file` object follows the context manager interface (implements the `__enter__` and `__exit__` method), the file handler itself will ensure that the file connection is closed no matter what happens in between.

## Reading

To read the content of a file, make sure to open the file handler with `r` permissions.

```python
with open('/path/to/your/file', 'r') as file_object:
    content = file_object.read()
```

In case of handling JSON data (as needed in this project), we should parse the file content using the built-in `json` library.

```python
with open('/path/to/your/file', 'r') as file_object:
    content = file_object.read()
    json_data = json.loads(content)  # loads JSON from a string
```

or

```python
with open('/path/to/your/file', 'r') as file_object:
    json_data = json.load(file_object)  # loads JSON from the file handler
```


## Writing

While writing, make sure to open the file handler with `w` or `a` permissions. Note that the `w` permission will drop all the content in the file while opening it. If you want to just append content to the current file without affecting the previous content, use the `a` permission instead.

```python
with open('/path/to/your/file', 'w') as file_object:  # this will clean the file content
    table_data = {'columns': columns, 'rows': []}
    json_data = json.dumps(table_data)  # serialize the python dict as a JSON valid string
    file_object.write(json_data)
```
