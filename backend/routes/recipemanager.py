from pydantic import BaseModel
from fastapi import APIRouter, Response, status, Cookie
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

def insert_steps(rid, data, connection, cursor):
    try:
        for i, step in enumerate(data):
            step_statement = (
                """INSERT INTO steps (rid, stepNr, description) VALUES (%s, %s, %s)"""
            )
            values = [rid, i + 1, step]
            cursor.execute(step_statement, values)

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error: {err}")
        raise mysql.connector.Error


def insert_ingredients(rid, data, connection, cursor):
    try:
        for ingredient in data:
            values = [rid, ingredient["name"], ingredient["amount"], ingredient["type"]]
            ingredient_statement = "INSERT INTO ingredients (rid, name, amount, type) VALUES(%s, %s, %s, %s)"
            cursor.execute(ingredient_statement, values)

    except mysql.connector.Error as err:
        connection.rollback()
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
        connection, cursor = get_connection()

        user = authenticate(token)
        if user is False:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {"message": "Invalid token"}

        uid = user["uid"]

        values = [data.recipename, data.description, data.ispublic, uid]

        statement = """INSERT INTO recipes (recipename, description, ispublic, uid) VALUES (%s, %s, %s, %s)"""

        cursor.execute(statement, values)

        rid = cursor.lastrowid

        insert_steps(rid, data.steps, connection, cursor)
        insert_ingredients(rid, data.ingredients, connection, cursor)

        response.status_code = status.HTTP_201_CREATED

        return {"message": f"recipe {data.recipename} created successfully"}

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"error{err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Internal server error"}
    
    finally:
        close_connections(connection, cursor)
    

def get_rids(ingredients, cursor):
    ingredient_map = ", ".join(["%s"] * len(ingredients))
    r_ids = f"""SELECT rid FROM ingredients WHERE name IN ({ingredient_map})"""

    cursor.execute(r_ids, ingredients)
    result = cursor.fetchall()

    rid_data = []
    for rid in result:
        rid_data.append(int(rid["rid"]))

    return rid_data


class FilterItem(BaseModel):
    recipename: str
    ingredients: list
    exclude_own: bool


@router.post("/api/getRecipes", status_code=200)
def get_recipes(
    data: FilterItem, response: Response, token: Annotated[str | None, Cookie()] = None
):
    try:
        connection, cursor = get_connection()

        statement = ''''''
        values = []

        if len(data.ingredients) < 1 and data.exclude_own is False:
            statement = """SELECT rid, recipename, description, uid FROM recipes WHERE recipename LIKE %s"""
            values = [f"%{data.recipename}%"]

        elif len(data.ingredients) < 1 and data.exclude_own is True:
            user = authenticate(token)

            if user is False:
                response.status_code = status.HTTP_403_FORBIDDEN
                return {"message": "Invalid token"}

            uid = user["uid"]

            statement = """SELECT rid, recipename, description, uid FROM recipes WHERE uid != %s AND recipename LIKE %s"""
            values = [uid, f"%{data.recipename}%"]

        elif len(data.ingredients) > 0 and data.exclude_own is False:
            param_data = get_rids(data.ingredients, cursor)

            if len(param_data) <= 0:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {"message": "No recipes found"}

            rids = ", ".join(["%s"] * len(param_data))

            statement = f"""SELECT rid, recipename, description, uid FROM recipes WHERE rid IN ({rids})
            AND recipename LIKE %s
            """
            param_data.append(f"%{data.recipename}%")
            values = param_data

        elif len(data.ingredients) > 0 and data.exclude_own is True:
            user = authenticate(token)

            if user is False:
                response.status_code = status.HTTP_403_FORBIDDEN
                return {"message": "Invalid token"}

            uid = user["uid"]

            uid = user['uid']
            
            param_data = get_rids(data.ingredients, cursor)

            if len(param_data) <= 0:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {"message": "No recipes found"}

            rids = ", ".join(["%s"] * len(param_data))

            statement = f"""SELECT rid, recipename, description, uid FROM recipes WHERE rid IN ({rids}) 
            AND uid != %s AND recipename LIKE %s
            """
            param_data.append(uid)
            param_data.append(f"%{data.recipename}%")
            values = param_data

        cursor.execute(statement, values)

        result = cursor.fetchall()

        response.status_code = status.HTTP_200_OK
        return result

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'message': "Internal server error"}
    
    finally:
        close_connections(connection, cursor)

def recipe_formatter(recipe):

    ingredient_list = []
    step_list = []

    seen_ingredients = []
    seen_steps = []

    for data in recipe:
        if data["name"] not in seen_ingredients:
            ingredient_list.append(
                {"name": data["name"], "amount": data["amount"], "type": data["type"]}
            )

            seen_ingredients.append(data["name"])

        if data["stepNr"] not in seen_steps:
            step_list.append(
                data["step_desc"]
            )

            seen_steps.append(data["stepNr"])

    recipe_data = {
        "rid": recipe[0]["rid"],
        "recipename": recipe[0]["recipename"],
        "description": recipe[0]["recipe_desc"],
        'ispublic': recipe[0]["ispublic"],
        "ingredients": ingredient_list,
        "steps": step_list,
    }

    return recipe_data


@router.get("/api/getRecipeDetailed/", status_code=200)
def get_detailed_recipe(response: Response, rid: int):
    try:
        connection, cursor = get_connection()

        statement = '''
            SELECT DISTINCT r.rid, r.recipename, r.description as recipe_desc, r.ispublic,
            i.name, i.amount, i.type, s.stepNr, s.description as step_desc FROM recipes r 
            INNER JOIN ingredients i ON r.rid = i.rid 
            INNER JOIN steps s ON r.rid = s.rid WHERE r.rid = %s
        '''

        cursor.execute(statement, [rid])

        result = cursor.fetchall()

        formatted = recipe_formatter(result)

        response.status_code = status.HTTP_200_OK
        return formatted

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'message': "Internal server error"}
    
    finally:
        close_connections(connection, cursor)
    
@router.get("/api/getTopRecepies", status_code = 200)
def get_top_recepies(response: Response):
    try:
        connection, cursor = get_connection()

        statement = '''
        SELECT f.rid, r.recipename, r.description, COUNT(f.rid) AS favoriteCount FROM favorites f 
        JOIN recipes r ON f.rid = r.rid GROUP BY f.rid ORDER BY favoriteCount desc LIMIT 10
        '''

        cursor.execute(statement)
        result = cursor.fetchall()

        return result

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {'message': "Internal server error"}
    
    finally:
        close_connections(connection, cursor)

@router.put("/api/editRecipe/", status_code=200)
def edit_recipe(
    data: CreateRecipe,
    response: Response,
    rid: int,
    token: Annotated[str | None, Cookie()],
):
    try:
        connection, cursor = get_connection()

        user = authenticate(token)
        if user is False:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {"message": "Invalid token"}
        
        get_creator = '''SELECT uid FROM recipes WHERE rid = %s'''
        cursor.execute(get_creator, [rid])
        owner = cursor.fetchone()

        if user['uid'] != owner['uid']:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'message': "You are not the owner of this recipe"}

        update_recipe = """UPDATE recipes SET recipename = %s, description = %s, ispublic = %s WHERE rid = %s"""
        update_values = [data.recipename, data.description, data.ispublic, rid]
        cursor.execute(update_recipe, update_values)

        delete_sub_statment = """DELETE s,i FROM steps s JOIN ingredients i ON s.rid = i.rid WHERE s.rid = %s"""
        cursor.execute(delete_sub_statment, [rid])

        insert_ingredients(rid, data.ingredients, connection, cursor)
        insert_steps(rid, data.steps, connection, cursor)

        response.status_code = status.HTTP_202_ACCEPTED
        return {"message": "Successfully updated recipe"}

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Internal server error"}
    
    finally:
        close_connections(connection, cursor)


@router.delete("/api/deleteRecipe/", status_code=200)
def delete_recipe(response: Response, p_rid: int, token: Annotated[str | None, Cookie()]):
    try:
        connection, cursor = get_connection()

        user = authenticate(token)
        if user is False:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {"message": "Invalid token"}

        uid = user["uid"]

        get_creator = '''SELECT uid FROM recipes WHERE rid = %s'''
        cursor.execute(get_creator, [p_rid])
        owner = cursor.fetchone()

        if uid != owner['uid']:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {'message': "You are not the owner of this recipe"}

        Values = [p_rid, uid]

        delete_recipe_statement = """DELETE FROM recipes WHERE rid = %s AND uid = %s"""
        delete_sub_statment = """DELETE s,i FROM steps s JOIN ingredients i ON s.rid = i.rid WHERE s.rid = %s"""

        cursor.execute(delete_sub_statment, [p_rid])
        cursor.execute(delete_recipe_statement, Values)

        if cursor.rowcount == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "Deletion failed, recipe not found"}
        else:
            response.status_code = status.HTTP_200_OK
            return {"message": "Successfully deleted recipe"}

    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Internal server error"}
    
    finally:
        close_connections(connection, cursor)


@router.get("/api/getAllRecipes", status_code=200)
def get_all_recipes(response: Response):
    try:
        connection, cursor = get_connection()

        statement = """SELECT rid, recipename, description, uid From recipes ORDER BY rid DESC"""
        cursor.execute(statement)
        result = cursor.fetchall()
        response.status_code = status.HTTP_200_OK
        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "Internal server error"}
    
    finally:
        close_connections(connection, cursor)
