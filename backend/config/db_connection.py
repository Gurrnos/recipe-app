import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode


load_dotenv()

config = {
            'user': os.getenv("DB_USER"),
            'host': os.getenv("DB_HOST"),
            'port': int(os.getenv("DB_PORT")),
            'password': os.getenv("DB_PASSWORD"),
            'database': os.getenv("DATABASE")
        }

try:
    cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_size = 5, autocommit = True, **config)

    print(f"Connected to db: {config['database']}")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Access denied error: Check your username and password to make sure they match")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")

    else:
        print(err)

def get_connection():
    connection = cnxpool.get_connection()

    cursor = connection.cursor(dictionary=True)

    return connection, cursor
