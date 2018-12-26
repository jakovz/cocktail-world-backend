#!/usr/bin/python
import json
import requests

LIST_INGREDIENTS_URL = 'https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list'
DRINK_BY_ID_URL = 'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i='
SPECIFIC_INGREDIENT_URL = 'https://www.thecocktaildb.com/api/json/v1/1/filter.php?i='
INGREDIENT_IMG_URL = 'https://www.thecocktaildb.com/images/ingredients/%s-Small.png'


def fill_drinks():
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

    for drinkId in ids:
        drinkRequest = requests.get(DRINK_BY_ID_URL + drinkId)
        drinkJson = drinkRequest.json()
        for drinkDetails in drinkJson['drinks']:
            print(drinkDetails['idDrink'], drinkDetails['strDrink'], drinkDetails['strCategory'],
                  drinkDetails['strIBA'], drinkDetails['strAlcoholic'], drinkDetails['strGlass'],
                  drinkDetails['strInstructions'], drinkDetails['strDrinkThumb'])
            for i in range(1, 13):
                drinkIngredient = drinkDetails['strIngredient' + str(i)]
                if drinkIngredient != '' and drinkIngredient != ' ' and drinkIngredient != '\n' and drinkIngredient != '\r\n' and drinkIngredient != None:
                    print(i, drinkIngredient)
                measure = drinkDetails['strMeasure' + str(i)]
                if measure != '' and measure != ' ' and measure != '\n' and measure != '\n' and measure != '\r\n' and measure != None:
                    print(i, measure)


def fill_ingredients():
    ingredients_list = requests.get(LIST_INGREDIENTS_URL).json()['drinks']
    for ingredient in ingredients_list:
        ingredient_name = ingredient['strIngredient1']
        ingredient_details = requests.get(SPECIFIC_INGREDIENT_URL + ingredient_name).json()['ingredients'][0]
        ingredient_id = ingredient_details['idIngredient']
        ingredient_description = ingredient_details['strDescription']
        ingredient_type = ingredient_details['strType']
        ingredient_img_url = INGREDIENT_IMG_URL % ingredient_name

        # TODO: should check that everything is returned correctly
        # TODO: execute the query that inserts the ingredient
        # TODO: add calories for each ingredient from Food Data API


if __name__ == '__main__':
    pass