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


class SignupItem(BaseModel):
    username: str
    email: str
    password: str

@router.post("/api/signup", tags=["users"], status_code = 201)
def signup(data: SignupItem, response: Response):
    try:
        if len(data.password) > 50:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'message': "Password exceeding character limit"}

        hashed_password = hashPassword(data.password.encode("utf-8"))

        statement = '''INSERT INTO users (username, email, password) VALUES (%s, %s, %s)'''

        values = data.username, data.email, hashed_password

        cursor.execute(statement, values)
        uid = cursor.lastrowid

        db.commit()

        response.status_code = status.HTTP_201_CREATED

        payload = {
                'uid': uid, 
                'username': data.username, 
                'email': data.email, 
                'exp': datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours = 4)
        }

        token = jwt.encode(payload, key, algorithm="HS256")
        print(token)
        #response.set_cookie(key='token', value=token, max_age = 3600 * 4)

        return {"message": f"User {data.username} created successfully"}

    except mysql.connector.Error as err:
        db.rollback()

        if err.errno == errorcode.ER_DUP_ENTRY:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": "A user with that email already exists"}
        else:
            print(f"error {err}")
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"message": "Internal server error"}
        

class LoginItem(BaseModel):
    email: str
    password: str

@router.post("/api/login", tags=["users"], status_code = 200)
def login(data: LoginItem, response: Response):
    try:
        statement = '''SELECT * FROM users WHERE email = %s'''
        values = [data.email]

        cursor.execute(statement, values)
        user = cursor.fetchone()

        if user is None:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {'message': "Invalid email or password"}
        
        elif checkPassword(data.password.encode("utf-8"), user['password'].encode("utf-8")) is False:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {'message': "Invalid email or password"}
        
        response.status_code = status.HTTP_200_OK

        payload = {
                'uid': user['uid'], 
                'username': user['username'], 
                'email': user['email'], 
                'exp': datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours = 4)
        }

        token = jwt.encode(payload, key, algorithm="HS256")
        print(token)
        #response.set_cookie(key='token', value=token, max_age = 3600 * 4)
        return {'message': f"Successfully logged in as {user['username']}"}

    except mysql.connector.Error as err:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(f"error {err}")
        return {'message': "Internal server error"}
    

class UpdateData (BaseModel):
    old_passw: str
    new_passw: str

@router.put("/api/changePassw", status_code = 200)
def chance_password(data: UpdateData, response: Response, token: Annotated[str | None, Cookie()]):
    try:
        user = authenticate(token)

        if user is False:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'message': "Invalid token"}

        uid = user['uid']

        values = [uid]
        statement = '''SELECT * from users WHERE uid = %s'''
        cursor.execute(statement, values)

        user = cursor.fetchone()

        if user is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'message': "User not found"}
        
        elif checkPassword(data.old_passw.encode("utf-8"), user['password'].encode("utf-8")) is False:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {'message': "Invalid password"}
        
        new_passw = hashPassword(data.new_passw.encode("utf-8"))
        update_statement = '''UPDATE users SET password = %s WHERE uid = %s'''
        new_values = [new_passw, uid]

        cursor.execute(update_statement, new_values)
        db.commit()

        response.status_code = status.HTTP_202_ACCEPTED
        return {'message': 'Successfully updated password'}
    
    except mysql.connector.Error as err:
        db.rollback()
        print(f"Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'message': "Internal server error"}


class UsernameItem (BaseModel):
    new_username: str

@router.put("/api/changeUsername", status_code = 200)
def change_username(data: UsernameItem, response: Response, token: Annotated[str | None, Cookie()]):
    try:
        user = authenticate(token)

        if user is False:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'message': "Invalid token"}

        uid = user['uid']

        values = [data.new_username, uid]
        statement = '''UPDATE users SET username = %s WHERE uid = %s'''

        cursor.execute(statement, values)
        db.commit()
        
        response.status_code = status.HTTP_202_ACCEPTED
        return {'message': "Successfully updated username"}

    except mysql.connector.Error as err:
        db.rollback()
        print(f"Error: {err}")

        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'message': "Internal server error"}
    

@router.delete("/api/deleteAccount", status_code = 200)
def delete_account(response: Response, token: Annotated[str | None, Cookie()]):
    try:
        user = authenticate(token)

        if user is False:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'message': "Invalid token"}

        uid = user['uid']

        values = [uid]
        statement = '''DELETE FROM users WHERE uid = %s'''

        cursor.execute(statement, values)
        db.commit()

        if cursor.rowcount == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {'message': 'Deletion failed, user not found'}
        else:
            response.status_code = status.HTTP_200_OK
            return {'message': 'Successfully deleted account'}

    except mysql.connector.Error as err:
        db.rollback()
        print(f"Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'message': 'Internal server error'}
    
