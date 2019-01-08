#!/usr/bin/python
import json
import requests
import DBConnection
import csv

LIST_INGREDIENTS_URL = 'https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list'
DRINK_BY_ID_URL = 'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i='
SPECIFIC_INGREDIENT_URL = 'https://www.thecocktaildb.com/api/json/v1/1/filter.php?i='
INGREDIENT_IMG_URL = 'https://www.thecocktaildb.com/images/ingredients/%s-Small.png'
INGREDIENT_URL = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?i='
LIST_MEALS_CATEGORIES_URL = 'https://www.themealdb.com/api/json/v1/1/list.php?c=list'
MEALS_BY_CATEGORY_URL = 'https://www.themealdb.com/api/json/v1/1/filter.php?c='
MEALS_BY_ID_URL = 'https://www.themealdb.com/api/json/v1/1/lookup.php?i='
LIST_MEALS_INGREDIENTS_URL = 'https://www.themealdb.com/api/json/v1/1/list.php?i=list'
MEALS_INGREDIENT_IMG_URL = 'https://www.themealdb.com/images/ingredients/%s-Small.png'
LIST_FOOD_CATEGORY = 'https://www.themealdb.com/api/json/v1/1/categories.php'

# fill drinks table 
InsertDrinksQuery = "INSERT INTO %s VALUES (%s, \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")"

# fill cocktails_ingredients table 
InsertCocktailsIngredientsQuery = "INSERT INTO %s VALUES (%s, \"%s\", \"%s\")"

# fill coctails ingredients in ingredients table
InsertIngredientsQuery = "INSERT INTO %s VALUES (\"%s\", \"%s\", \"%s\", \"%s\", %s)"

# fill meals table 
InsertMealsQuery = "INSERT INTO %s VALUES (%s, \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")"

# fill food_categories table
InsertFoodCategoryQuery = "INSERT INTO %s VALUES (%s, \"%s\", \"%s\", \"%s\")"

# fill calories column in ingredients table
UPDATE_INGREDIENT_CALORIES = "UPDATE %s SET calories = \"%s\" WHERE ingredient_name = \"%s\""

# get all ingredients
GET_INGREDIENTS_LIST = "SELECT ingredient_name FROM ingredients"


def fill_drinks():
    # create dictionary of all coctails id (ids[id, 1])
    ingredientListRequest = requests.get(LIST_INGREDIENTS_URL)
    ingredientListJson = ingredientListRequest.json()
    ids = {}
    for ingredients in ingredientListJson['drinks']:
        ingredientType = ingredients['strIngredient1'].replace(" ", "_")
        print(ingredientType)
        ingredientRequest = requests.get(SPECIFIC_INGREDIENT_URL + ingredientType)
        ingredientJson = ingredientRequest.json()
        for ingredient in ingredientJson['drinks']:
            idDrink = ingredient['idDrink']
            if idDrink not in ids:
                ids[idDrink] = 1 
    # fill drinks table 
    for drinkId in ids:
        drinkRequest = requests.get(DRINK_BY_ID_URL + drinkId)
        drinkJson = drinkRequest.json()
        for drinkDetails in drinkJson['drinks']:
            idDrink = drinkDetails['idDrink']
            strDrink = drinkDetails['strDrink'].replace("\"", "\'")
            strCategory = drinkDetails['strCategory']
            strIBA = drinkDetails['strIBA']
            strAlcoholic = drinkDetails['strAlcoholic']
            strGlass = drinkDetails['strGlass']
            strInstructions = drinkDetails['strInstructions'].replace("\"", "\'").encode("latin-1", "ignore").decode("utf-8", "ignore")
            strDrinkThumb = drinkDetails['strDrinkThumb']
            print(idDrink, strDrink, strCategory, strIBA, strAlcoholic, strGlass, strInstructions, strDrinkThumb)
            DBConnection.execute_query(InsertDrinksQuery, 'drinks', idDrink, strDrink, strCategory, strIBA, strAlcoholic, strGlass, strInstructions, strDrinkThumb)

            # fill cocktails_ingredients table 
            for i in range(1, 13):
                ingredientIsNotNull = False
                drinkIngredient = drinkDetails['strIngredient' + str(i)]
                if drinkIngredient != '' and drinkIngredient != ' ' and drinkIngredient != '\n' and drinkIngredient != '\r\n' and drinkIngredient != None:
                    ingredientIsNotNull = True
                    print(i, drinkIngredient)
                    drinkIngredientRequest = requests.get(INGREDIENT_URL + drinkIngredient)
                measure = drinkDetails['strMeasure' + str(i)]
                if measure != '' and measure != ' ' and measure != '\n' and measure != '\n' and measure != '\r\n' and measure != None:
                    print(i, measure)
                if ingredientIsNotNull:
                    print(i, idDrink, drinkIngredient, measure)
                    DBConnection.execute_query(InsertCocktailsIngredientsQuery, 'cocktails_ingredients', idDrink, drinkIngredient, measure)


def fill_ingredients():
    ingredients_list = requests.get(LIST_INGREDIENTS_URL).json()['drinks']
    for ingredient in ingredients_list:
        ingredient_name = ingredient['strIngredient1']
        ingredient_request = requests.get(INGREDIENT_URL + ingredient_name)
        ingredient_details = ingredient_request.json()['ingredients'][0]
        ingredient_id = ingredient_details['idIngredient']
        ingredient_description = ingredient_details['strDescription']
        if ingredient_description is not None:
            ingredient_description = ingredient_description.replace("\"", "\'").encode("latin-1", "ignore").decode("utf-8", "ignore")
        ingredient_type = ingredient_details['strType']
        ingredient_img_url = INGREDIENT_IMG_URL % ingredient_name
        print(ingredient_name, ingredient_id, ingredient_description, ingredient_type, ingredient_img_url)
        DBConnection.execute_query(InsertIngredientsQuery, 'ingredients', ingredient_name, ingredient_description, ingredient_type, ingredient_img_url, 0)

def fill_meals():
    # create dictionary of all meals id (ids[id, 1])
    mealsCategoryListJson = requests.get(LIST_MEALS_CATEGORIES_URL).json()
    ids = {}
    for category in mealsCategoryListJson['meals']:
        mealsCategory = category['strCategory']
        print(mealsCategory)
        mealsJson = requests.get(MEALS_BY_CATEGORY_URL + mealsCategory).json()
        for meal in mealsJson['meals']:
            idMeal = meal['idMeal']
            if idMeal not in ids:
                ids[idMeal] = 1 
    # fill meals table 
    for idMeals in ids:
        mealsJson = requests.get(MEALS_BY_ID_URL + idMeals).json()
        for mealsDetails in mealsJson['meals']:
            idMeal = mealsDetails['idMeal']
            strMeal = mealsDetails['strMeal']
            strCategory = mealsDetails['strCategory']
            strArea = mealsDetails['strArea']
            strInstructions = mealsDetails['strInstructions'].replace("\"", "\'").encode("latin-1", "ignore").decode("utf-8", "ignore")
            strMealThumb = mealsDetails['strMealThumb']
            strTags = mealsDetails['strTags']
            strYoutube = mealsDetails['strYoutube']
            print(idMeal, strMeal, strCategory, strArea, strInstructions, strMealThumb, strTags, strYoutube)
            DBConnection.execute_query(InsertMealsQuery, 'meals', idMeal, strMeal, strCategory, strArea, strInstructions, strMealThumb, strTags, strYoutube)

            # fill meals_ingredients table 
            for i in range(1, 20):
                ingredientIsNotNull = False
                mealsIngredient = mealsDetails['strIngredient' + str(i)]
                if mealsIngredient != '' and mealsIngredient != ' ' and mealsIngredient != '\n' and mealsIngredient != '\r\n' and mealsIngredient != None:
                    ingredientIsNotNull = True
                    print(i, mealsIngredient)
                    idIngredient = 5
                measure = mealsDetails['strMeasure' + str(i)]
                if measure != '' and measure != ' ' and measure != '\n' and measure != '\n' and measure != '\r\n' and measure != None:
                    print(i, measure)
                if ingredientIsNotNull:
                    print(i, idMeal, mealsIngredient, measure)
                    DBConnection.execute_query(InsertCocktailsIngredientsQuery, 'meal_ingredients', idMeal, mealsIngredient, measure)


def fill_meals_ingredients():
    ingredients_list = requests.get(LIST_MEALS_INGREDIENTS_URL).json()['meals']
    for ingredient in ingredients_list:
        ingredient_name = ingredient['strIngredient']
        ingredient_id = ingredient['idIngredient']
        ingredient_description = ingredient['strDescription']
        if ingredient_description is not None:
            ingredient_description = ingredient_description
        ingredient_type = ingredient['strType']
        ingredient_img_url = MEALS_INGREDIENT_IMG_URL % ingredient_name
        print(ingredient_name, ingredient_id, ingredient_description, ingredient_type, ingredient_img_url)
        DBConnection.execute_query(InsertIngredientsQuery, 'ingredients', ingredient_name, ingredient_description, ingredient_type, ingredient_img_url, 0)

def fill_food_categories():
    food_categories_list = requests.get(LIST_FOOD_CATEGORY).json()['categories']
    for category in food_categories_list:
        category_name = category['strCategory']
        category_id = category['idCategory']
        category_description = category['strCategoryDescription'].replace("\"", "\'").encode("latin-1", "ignore").decode("utf-8", "ignore")
        category_img_url = category['strCategoryThumb']
        print(category_name, category_id, category_description, category_img_url)
        DBConnection.execute_query(InsertFoodCategoryQuery, 'food_categories', category_id, category_name, category_img_url, category_description)

def fill_ingredients_calories():
    # create dictionary of all products (products[product_name, calories]) from csv
    products = {}
    with open('en.openfoodfacts.org.products.csv', encoding="utf8", errors='ignore') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            # row[7] - product_name
            # row[68] - energy_100g (kj)
            try:
                products[row[7]] = row[68]
            except Exception as e:
                    print(e)

    # get all ingredients from DB
    ingredient_list = DBConnection.execute_query(GET_INGREDIENTS_LIST)
    # find the ingredient in products
    ingredient_json = json.loads(ingredient_list)
    for ingredient in ingredient_json:
        ingredient_name = ingredient["ingredient_name"]
        print(ingredient_name)
        calories = products.get(ingredient_name)
        if calories is None or calories is '' or calories is ' ' or calories is '\n' or calories is '\r\n':
            for key, value in products.items():
                    if ingredient_name in key: 
                        calories = value
                        if calories is not '' and calories is not None and calories is not ' ' or calories is not '\n' or calories is not '\r\n':
                            break
        print(calories)
        
        try:
            DBConnection.execute_query(UPDATE_INGREDIENT_CALORIES, "ingredients", calories, ingredient_name)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    pass
