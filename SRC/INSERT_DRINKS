#!/usr/bin/python

import json
import requests
# from DBConnection.py 

ingredientListUrl = 'https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list'
ingredientListRequest = requests.get(ingredientListUrl)
ingredientListJson = ingredientListRequest.json()
ingredientUrl = 'https://www.thecocktaildb.com/api/json/v1/1/filter.php?i='
ids = {}
for ingredients in ingredientListJson['drinks']:
    ingredientType = ingredients['strIngredient1'].replace(" ", "_")
    print(ingredientType)
    ingredientRequest = requests.get(ingredientUrl+ingredientType)
    ingredientJson = ingredientRequest.json()
    for ingredient in ingredientJson['drinks']: 
        idDrink = ingredient['idDrink']
        if idDrink not in ids:
            ids[idDrink] = 1            
            
drinkIdUrl = 'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i='
InsertDrinksQuery = "INSERT INTO %s VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
InsertIngredientsQuery = "INSERT INTO %s VALUES (%s, %s, %s, )"

for drinkId in ids:
    drinkRequest = requests.get(drinkIdUrl+drinkId)
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
        execute_query(query, 'drinks', idDrink, strDrink, strCategory, strIBA, strAlcoholic, strGlass, strInstructions, strDrinkThumb):
#         for i in range(1, 13):
#             ingredientIsNotNull = false
#             drinkIngredient = drinkDetails['strIngredient'+str(i)]
#             if drinkIngredient != '' and drinkIngredient != ' ' and drinkIngredient != '\n' and drinkIngredient != '\r\n' and drinkIngredient != None:
#                 print(i, drinkIngredient)
#                 ingredientIsNotNull = true
#             measure = drinkDetails['strMeasure'+str(i)]
#             if measure != '' and measure != ' ' and measure != '\n' and measure != '\n' and measure != '\r\n'  and measure != None:
#                 print(i, measure)
#             if ingredientIsNotNull:
#                 execute_query(query, 'cocktails_ingredients', idDrink, drinkIngredient, measure)
                
    
