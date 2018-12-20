#!/usr/bin/python

import json
import requests

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

for drinkId in ids:
    drinkRequest = requests.get(drinkIdUrl+drinkId)
    drinkJson = drinkRequest.json()
    for drinkDetails in drinkJson['drinks']:
        print(drinkDetails['idDrink'],drinkDetails['strDrink'],drinkDetails['strCategory'],drinkDetails['strIBA'],drinkDetails['strAlcoholic'],drinkDetails['strGlass'],drinkDetails['strInstructions'],drinkDetails['strDrinkThumb'])
        for i in range(1, 13):
            drinkIngredient = drinkDetails['strIngredient'+str(i)]
            if drinkIngredient != '' and drinkIngredient != ' ' and drinkIngredient != '\n' and drinkIngredient != '\r\n' and drinkIngredient != None:
                print(i, drinkIngredient)
            measure = drinkDetails['strMeasure'+str(i)]
            if measure != '' and measure != ' ' and measure != '\n' and measure != '\n' and measure != '\r\n'  and measure != None:
                print(i, measure)
