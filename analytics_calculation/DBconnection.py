import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None

    try:
        connection = sqlite3.connect(path)
        if connection:
            print("success")
    except Error as e:
        print(f"The error {e} occurred, idk how to fix, google it")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def insert_into(table_name, column_names, item_list, path):
    start = f"""INSERT INTO {table_name} ({', '.join(column_names)}) Values """
    for item in item_list:
        item_str = ', '.join(item)
        start += f"""({item_str}), """
    start = start[:-2] + ';'
    connection = create_connection(path)
    execute_query(connection, start)
