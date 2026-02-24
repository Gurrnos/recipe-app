from pydantic import BaseModel
from fastapi import APIRouter, Response, status, Cookie
from config.db_connection import get_db
import mysql.connector
from mysql.connector import errorcode
from services.password import hashPassword, checkPassword
import jwt
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


class CreateRecipe(BaseModel):
    recipename: str
    description: str
    ispublic: int
    steps: list


@router.post("/api/createRecipe", tags=["recipes"], status_code=201)
def createRecipe(
    data: CreateRecipe, response: Response, token: Annotated[str | None, Cookie()]
):
    try:
        user = authenticate(token)
        if user is False:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {"message": "Invalid token"}

        uid = user["uid"]

        values = [data.recipename, data.description, data.ispublic, uid]

        statement = """INSERT INTO recipes (recipename, description, ispublic, uid) VALUES (%s, %s, %s, %s)"""

        cursor.execute(statement, values)
        rid = cursor.lastrowid

        db.commit()
        response.status_code = status.HTTP_201_CREATED

        return {"message": f"recipe {data.recipename} created successfully"}

    except mysql.connector.Error as err:
        db.rollback()
        print(f"error{err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Internal server error"}


@router.delete("/api/deleteRecipe", status_code=200)
def delete_recipe(response: Response, token: Annotated[str | None, Cookie()]):
    try:
        user = authenticate(token)
        if user is False:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {"message": "Invalid token"}

        uid = user["uid"]
        rid = 5  # TODO HARDBAKED VALUE CHANGE WHEN UI IMPLEMENTED
        Values = [rid, uid]
        statement = """DELETE FROM recipes WHERE rid = %s AND uid = %s"""

        cursor.execute(statement, Values)
        db.commit()

        if cursor.rowcount == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "Deletion failed, recipe not found"}
        else:
            response.status_code = status.HTTP_200_OK
            return {"message": "Successfully deleted recipe"}

    except mysql.connector.Error as err:
        db.rollback()
        print(f"Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Internal server error"}
