from pydantic import BaseModel
from fastapi import APIRouter, Response, status, Cookie
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


def insert_steps(rid, data):
    try:
        for i, step in enumerate(data):
            step_statement = (
                """INSERT INTO steps (rid, stepNr, description) VALUES (%s, %s, %s)"""
            )
            values = [rid, i + 1, step]
            cursor.execute(step_statement, values)

    except mysql.connector.Error as err:
        db.rollback()
        print(f"Error: {err}")
        raise mysql.connector.Error


def insert_ingredients(rid, data):
    try:
        for ingredient in data:
            values = [rid, ingredient["name"], ingredient["amount"], ingredient["type"]]
            ingredient_statement = "INSERT INTO ingredients (rid, name, amount, type) VALUES(%s, %s, %s, %s)"
            cursor.execute(ingredient_statement, values)

    except mysql.connector.Error as err:
        db.rollback()
        print(f"Error: {err}")
        raise mysql.connector.Error


class CreateRecipe(BaseModel):
    recipename: str
    description: str
    ispublic: int
    ingredients: list
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

        insert_steps(rid, data.steps)
        insert_ingredients(rid, data.ingredients)

        db.commit()
        response.status_code = status.HTTP_201_CREATED

        return {"message": f"recipe {data.recipename} created successfully"}

    except mysql.connector.Error as err:
        db.rollback()
        print(f"error{err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Internal server error"}


def recipe_formatter(recipe):

    ingredient_list = []
    step_list = []

    seen_ingredients = []
    seen_steps = []

    for data in recipe:
        if data['name'] not in seen_ingredients:
            ingredient_list.append({'name': data['name'], 'amount': data['amount'], 'type': data['type']})
        
            seen_ingredients.append(data['name'])

        if data['stepNr'] not in seen_steps:
            step_list.append({'stepNr': data['stepNr'], 'description': data['step_desc']})

            seen_steps.append(data['stepNr'])

    recipe_data = {
        'rid': recipe[0]['rid'],
        'recipename': recipe[0]['recipename'], 
        'description': recipe[0]['recipe_desc'],
        'ingredients': ingredient_list,
        'steps': step_list
    }

    return recipe_data



@router.get("/api/getRecipeDetailed/", status_code = 200)
def get_detailed_recipe(response: Response, rid: int):
    try:
        statement = '''
            SELECT DISTINCT r.rid, r.recipename, r.description as recipe_desc, 
            i.name, i.amount, i.type, s.stepNr, s.description as step_desc FROM recipes r 
            INNER JOIN ingredients i ON r.rid = i.rid 
            INNER JOIN steps s ON r.rid = s.rid WHERE r.rid = %s
        '''

        cursor.execute(statement, [rid])

        result = cursor.fetchall()

        formatted = recipe_formatter(result)

        response.status_code = status.HTTP_200_OK
        return {'message': f"data: {formatted}"}

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'message': "Internal server error"}

@router.delete("/api/deleteRecipe", status_code=200)
def delete_recipe(response: Response, token: Annotated[str | None, Cookie()]):
    try:
        user = authenticate(token)
        if user is False:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {"message": "Invalid token"}

        uid = user["uid"]
        rid = 14  # TODO HARDBAKED VALUE CHANGE WHEN UI IMPLEMENTED
        Values = [rid, uid]

        delete_recipe_statement = """DELETE FROM recipes WHERE rid = %s AND uid = %s"""
        delete_sub_statment = """DELETE s,i FROM steps s JOIN ingredients i ON s.rid = i.rid WHERE s.rid = %s"""

        cursor.execute(delete_sub_statment, [rid])
        cursor.execute(delete_recipe_statement, Values)
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


@router.put("/api/editRecipe", status_code=200)
def edit_recipe(
    data: CreateRecipe, response: Response, token: Annotated[str | None, Cookie()]
):
    try:
        user = authenticate(token)
        if user is False:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {"message": "Invalid token"}

        rid = 18  # TODO HARDBAKED VALUE CHANGE WHEN UI IMPLEMENTED FETCH CORRECT RECIPE ID

        update_recipe = """UPDATE recipes SET recipename = %s, description = %s, ispublic = %s WHERE rid = %s"""
        update_values = [data.recipename, data.description, data.ispublic, rid]
        cursor.execute(update_recipe, update_values)

        delete_sub_statment = """DELETE s,i FROM steps s JOIN ingredients i ON s.rid = i.rid WHERE s.rid = %s"""
        cursor.execute(delete_sub_statment, [rid])

        insert_ingredients(rid, data.ingredients)
        insert_steps(rid, data.steps)

        db.commit()
        response.status_code = status.HTTP_202_ACCEPTED
        return {"message": "Successfully updated recipe"}

    except mysql.connector.Error as err:
        db.rollback()
        print(f"Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Internal server error"}
