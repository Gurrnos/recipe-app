from pydantic import BaseModel
from fastapi import APIRouter, Response, status
from config.db_connection import get_db
import mysql.connector
from mysql.connector import errorcode
from services.password import hashPassword, checkPassword

router = APIRouter()
db = get_db()
cursor = db.cursor(dictionary=True)

class SignupItem(BaseModel):
    username: str
    email: str
    password: str

@router.post("/signup", tags=["users"], status_code = 201)
def signup(data: SignupItem, response: Response):
    try:
        if len(data.password) > 50:
            return {'message': "Password exceeding character limit"}

        hashed_password = hashPassword(data.password.encode("utf-8"))

        statement = '''INSERT INTO users (username, email, password) VALUES (%s, %s, %s)'''

        values = data.username, data.email, hashed_password

        cursor.execute(statement, values)

        db.commit()

        response.status_code = status.HTTP_201_CREATED
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
        
#TODO: FIX TOKEN FOR LOGIN AND CHANGE PASSWORD!!!

class LoginItem(BaseModel):
    email: str
    password: str

@router.post("/login", tags=["users"], status_code = 200)
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
        return {'message': f"Successfully logged in as {user['username']}"}
    


    except mysql.connector.Error as err:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(f"error {err}")
        return {'message': "Internal server error"}
    

class UpdateData (BaseModel):
    old_passw: str
    new_passw: str

@router.put("/changePassw")
def chance_password(data: UpdateData, response: Response, status_code = 200):
    try:
        uid = 'get uid from token'

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

        return {'message': 'Successfully updated password'}
    
    except mysql.connector.Error as err:
        db.rollback()
        print(f"Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'message': "Internal server error"}



@router.delete("/deleteAccount", status_code = 200)
def delete_account(response: Response):
    try:
        uid = 'get uid from token'

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
    
