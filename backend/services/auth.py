from config.db_connection import get_db
import jwt
import os
from dotenv import load_dotenv

db = get_db()
cursor = db.cursor(dictionary=True)
load_dotenv()


def authenticate(cookie):
    print(cookie)

    if cookie is None:
        return False

    try:
        user = jwt.decode(cookie, os.getenv("JWT_SECRET"), algorithms="HS256")
        print(user)

        return user

    except Exception as e:
        print(f"Decoding error: {e}")
        return False
