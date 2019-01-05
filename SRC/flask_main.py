from flask import Flask, request
from flask_cors import CORS
import json
import DBConnection
import queries

app = Flask(__name__)
CORS(app)

AVAILABLE_FILTERS = ["Calories"]


@app.route('/')
def main_page():
    return 'Hello World!'


# return: A json representing all the ingredients exist in the DB.
@app.route('/ingredients')
def get_ingredients():
    all_ingredients = DBConnection.execute_query(queries.all_ingredient_names)
    ingredients_names_list = [ingredient['name'] for ingredient in json.loads(all_ingredients)]
    ingredients_dict = {"ingredients": ingredients_names_list}
    return json.dumps(ingredients_dict)



@app.route('/calories_alcoholic')


@app.route('/cocktail_amount_by_glass_categories')
def get_cocktail_amount_by_glass_categories():
    glass_categories = DBConnection.execute_query(queries.query_cocktail_amount_by_glass_categories(["Ordinary Drink", "Shot"], True))
    return json.dumps()


@app.route('/ingredients_difference')
def get_ingredients_difference():
    ingredients_difference = DBConnection.execute_query(queries.query_ingredients_difference(10, 10))
    return json.dumps()


@app.route('/most_used_non_alcoholic')
def get_most_used_non_alcoholic():
    glass_categories = DBConnection.execute_query(queries.query_most_used_non_alcoholic())
    return json.dumps()


@app.route('/categories_by_average_number_of_ingredients')
def get_categories_by_average_number_of_ingredients():
    glass_categories = DBConnection.execute_query(queries.categories_by_average_number_of_ingredients(["Ordinary Drink", "Shot"]))
    return json.dumps()

@app.route('/easy_to_make_from_category')
def get_easy_to_make_from_category():
    glass_categories = DBConnection.execute_query(queries.query_easy_to_make_from_category("Beef", "Shot"))
    return json.dumps()

@app.route('/full_text_search')


@app.route('/common_ingredients')


if __name__ == '__main__':
    app.run(debug=True, port="8000")
    app.run(threaded=True)  # GOOD YUVAL
