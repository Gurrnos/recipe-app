from pydantic import BaseModel
from fastapi import APIRouter, Response, status, Cookie, HTTPException
from config.db_connection import get_db
import mysql.connector
from mysql.connector import errorcode
from services.password import hashPassword, checkPassword
import jwt
import json
import os
from dotenv import load_dotenv
from services.auth import authenticate
from typing import Annotated
from datetime import timezone
import time, datetime

load_dotenv()
router = APIRouter()
db = get_db()
cursor = db.cursor(dictionary=True)
key = os.getenv("JWT_SECRET")


class Favorite(BaseModel):
    uid: int
    rid: int


@router.post("/api/users/toggleFavorite/", status_code=201)
def add_fav(response: Response, rid: int, token: Annotated[str | None, Cookie()]):
    try:
        user = authenticate(token)
        if user is False:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {"message": "invalid token"}

        CHECK_STATEMENT = """SELECT 1 FROM favorites WHERE uid=%s AND rid=%s"""
        cursor.execute(CHECK_STATEMENT, [user["uid"], rid])

        if cursor.fetchone():
            toggleStatement = """DELETE FROM favorites WHERE uid=%s AND rid=%s"""
            message = f"Removed Recipe with ID: {rid} from favorites"
        else:
            toggleStatement = """INSERT INTO favorites(uid, rid) VALUES(%s, %s) """
            message = f"Added Recipe with ID: {rid} to favorites"

        cursor.execute(toggleStatement, [user["uid"], rid])

        db.commit()
        response.status_code = status.HTTP_200_OK

        return {"message": message}

    except mysql.connector.Error as err:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(f"error {err}")
        return {"message": "Internal server error"}
