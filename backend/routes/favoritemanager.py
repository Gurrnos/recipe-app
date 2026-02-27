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


@router.get("/api/users/getFavorites", status_code = 200)
def get_favorites(response: Response, token: Annotated[str | None, Cookie()]):
    try:
        user = authenticate(token)

        if user is False:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'message': "Invalid token"}
        
        uid = user['uid']

        statement = '''
            SELECT f.rid, r.recipename, r.description FROM favorites f 
            JOIN recipes r ON f.rid = r.rid WHERE f.uid = %s;
        '''
        
        cursor.execute(statement, [uid])
        result = cursor.fetchall()

        if len(result) <= 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'message': "No favorites found"}

        return {'message': result}

    except mysql.connector.Error as err:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(f"error {err}")
        return {"message": "Internal server error"}