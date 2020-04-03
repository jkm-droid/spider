import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine

"""
function to establish connection to the database
"""


def dbconnect():
    # mysql connect database connection credentials
    DBHOST = 'localhost'
    DBNAME = 'spider'
    DBUSER = 'root'
    DBPASS = ''

    # try establishing connection to the database
    # throw errors if connection fails
    try:
        # dialect + driver: // username: password @ host:port / database
        # connecting using sqlalchemy
        connection = create_engine("mysql+mysqldb://root@localhost/spider")
        if connection:
            print("Connection established successfully")

        # connecting using mysql connect
        # connection = mysql.connector.connect(host=DBHOST, database=DBNAME, user=DBUSER, passwd=DBPASS)
        # if connection.is_connected():
        #   db_info = connection.get_server_info()
        #   print(f'Connected successfully to mysql version {db_info}')

        return connection

    except Error as e:
        print(f'{e}')
