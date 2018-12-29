#!/usr/bin/python
import json
import requests
import DBConnection

LIST_INGREDIENTS_URL = 'https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list'
DRINK_BY_ID_URL = 'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i='
SPECIFIC_INGREDIENT_URL = 'https://www.thecocktaildb.com/api/json/v1/1/filter.php?i='
INGREDIENT_IMG_URL = 'https://www.thecocktaildb.com/images/ingredients/%s-Small.png'
INGREDIENT_URL = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?i='

InsertDrinksQuery = "INSERT INTO %s VALUES (%s, \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")"
InsertCocktailsIngredientsQuery = "INSERT INTO %s VALUES (%s, %s, \"%s\")"
InsertIngredientsQuery = "INSERT INTO %s VALUES (%s, \"%s\", \"%s\", \"%s\", \"%s\", %s)"


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
            strDrink = drinkDetails['strDrink']
            strCategory = drinkDetails['strCategory']
            strIBA = drinkDetails['strIBA']
            strAlcoholic = drinkDetails['strAlcoholic']
            strGlass = drinkDetails['strGlass']
            strInstructions = drinkDetails['strInstructions']
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
                    try:
                        drinkIngredientJson = drinkIngredientRequest.json()['ingredients'][0]
                        idIngredient = drinkIngredientJson['idIngredient']
                    except TypeError as e:
                        ingredientIsNotNull = False
                        print(e)
                        print("Error: failed convert data to json (json null)")
                measure = drinkDetails['strMeasure' + str(i)]
                if measure != '' and measure != ' ' and measure != '\n' and measure != '\n' and measure != '\r\n' and measure != None:
                    print(i, measure)
                if ingredientIsNotNull:
                    print(i, idDrink, drinkIngredient, idIngredient, measure)
                    DBConnection.execute_query(InsertCocktailsIngredientsQuery, 'cocktails_ingredients', idDrink, idIngredient, measure)


def fill_ingredients():
    ingredients_list = requests.get(LIST_INGREDIENTS_URL).json()['drinks']
    for ingredient in ingredients_list:
        ingredient_name = ingredient['strIngredient1']
        ingredient_request = requests.get(INGREDIENT_URL + ingredient_name)
        ingredient_details = ingredient_request.json()['ingredients'][0]
        ingredient_id = ingredient_details['idIngredient']
        ingredient_description = ingredient_details['strDescription']
        ingredient_type = ingredient_details['strType']
        ingredient_img_url = INGREDIENT_IMG_URL % ingredient_name
        print(ingredient_name, ingredient_id, ingredient_description, ingredient_type, ingredient_img_url)
        DBConnection.execute_query(InsertIngredientsQuery, 'ingredients', ingredient_id, ingredient_name, ingredient_description, ingredient_type, ingredient_img_url, 0)
        # TODO: should check that everything is returned correctly
        # TODO: execute the query that inserts the ingredient
        # TODO: add calories for each ingredient from Food Data API

fill_ingredients()

if __name__ == '__main__':
    pass
