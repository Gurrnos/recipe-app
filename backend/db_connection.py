import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

load_dotenv()

def connect_db():

    try:
        config = {
            'user': os.getenv("DB_USER"),
            'host': os.getenv("DB_HOST"),
            'port': int(os.getenv("DB_PORT")),
            'password': os.getenv("DB_PASSWORD")
        }


        cnx = mysql.connector.connect(**config)

        print(f"Connection made to user: {config['user']} on port: {config['port']}")
    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")

        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")

        else:
            print(err)

    else:
        cnx.close()