from pydantic import BaseModel
from fastapi import APIRouter, Response, status, Cookie, HTTPException
from config.db_connection import get_connection
import mysql.connector
import os
from dotenv import load_dotenv
from services.auth import authenticate
from typing import Annotated

load_dotenv()
router = APIRouter()
key = os.getenv("JWT_SECRET")

def close_connections(connection, cursor):
    if connection:
        connection.close()

    if cursor:
        cursor.close()

@router.post("/api/users/toggleFavorite/", status_code=201)
def add_fav(response: Response, p_rid: int, token: Annotated[str | None, Cookie()]):
    try:
        connection, cursor = get_connection()

        user = authenticate(token)
        if user is False:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {"message": "invalid token"}

        toggle_statement = """CALL toggleFavorite(%s, %s, @result)"""

        cursor.execute(toggle_statement, (user["uid"], p_rid))

        cursor.execute("SELECT @result AS toggle_result")

        result = cursor.fetchone()["toggle_result"]

        print(result)
        if result == 1:
            message = f"Added Recipe with ID: {p_rid} to favorites"
        else:
            message = f"Removed Recipe with ID: {p_rid} from favorites"

        response.status_code = status.HTTP_200_OK
        return {"message": message}

    except mysql.connector.Error as err:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(f"error {err}")
        return {"message": "Internal server error"}
    
    finally:
        close_connections(connection, cursor)


@router.get("/api/users/getFavorites", status_code=200)
def get_favorites(response: Response, token: Annotated[str | None, Cookie()]):
    try:
        connection, cursor = get_connection()
        user = authenticate(token)

        if user is False:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {"message": "Invalid token"}

        uid = user["uid"]

        statement = """
            SELECT f.rid, r.recipename, r.description FROM favorites f 
            JOIN recipes r ON f.rid = r.rid WHERE f.uid = %s;
        """

        cursor.execute(statement, [uid])
        result = cursor.fetchall()

        if len(result) <= 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "No favorites found"}

        return result

    except mysql.connector.Error as err:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(f"error {err}")
        return {"message": "Internal server error"}
    
    finally:
        close_connections(connection, cursor)



@router.get("/api/users/getUserRecipes/", status_code=200)
def get_user_recipes(
    response: Response,
    own: bool,
    uid: int = None,
    token: Annotated[str | None, Cookie()] = None,
):
    try:
        connection, cursor = get_connection()
        print(own, token)

        if own is True:
            user = authenticate(token)

            if user is False:
                response.status_code = status.HTTP_403_FORBIDDEN
                return {"message": "Invalid token"}

            uid = user["uid"]

        if uid is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "No valid uid"}

        statement = (
            """SELECT rid, recipename, description FROM recipes WHERE uid = %s"""
        )
        cursor.execute(statement, [uid])

        result = cursor.fetchall()

        if len(result) <= 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "No recipes found for that user"}

        return result

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Internal server error"}

    finally:
        close_connections(connection, cursor)