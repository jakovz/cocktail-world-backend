from flask import Flask, request
from flask_cors import CORS
import json
import DBConnection
import queries

app = Flask(__name__)
CORS(app)


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


@app.route('/cocktail_categories')
def get_cocktail_categories():
    cocktail_categories = DBConnection.execute_query(queries.get_drinks_categories())
    cocktail_categories = [category['category'] for category in json.loads(cocktail_categories)]
    categories_dict = {"allowed_cocktail_categories": cocktail_categories}
    return json.dumps(categories_dict)


@app.route('/glass_types')
def get_glass_categories():
    glass_categories = DBConnection.execute_query(queries.get_glasses_types())
    glass_categories = [category['glass_type'] for category in json.loads(glass_categories)]
    categories_dict = {"glass_types": glass_categories}
    return json.dumps(categories_dict)


@app.route('/calories_alcoholic')
def get_calories_alcoholic():
    pass


@app.route('/cocktail_amount_by_glass_categories')
def get_cocktail_amount_by_glass_categories():
    if 'categories' not in request.args:
        return
    categories = request.args.get('categories')
    categories = json.loads(categories)
    glass_categories = DBConnection.execute_query(
        queries.query_cocktail_amount_by_glass_categories(categories, True))
    glass_categories_dict = {'categories_count': glass_categories}
    return json.dumps(glass_categories_dict)


@app.route('/ingredients_difference')
def get_ingredients_difference():
    if ('different_drinks' not in request.args) or ('ingredients_in_drink' not in request.args):
        return
    different_drinks = request.args.get('different_drink')
    ingredients_in_drink = request.args.get('ingredients_in_drink')
    ingredients_difference = DBConnection.execute_query(
        queries.query_ingredients_difference(different_drinks, ingredients_in_drink))
    ingredients_difference_dict = {'ingredients': ingredients_difference}
    return json.dumps(ingredients_difference_dict)


@app.route('/most_used_non_alcoholic')
def get_most_used_non_alcoholic():
    most_used_glass = DBConnection.execute_query(queries.query_most_used_non_alcoholic())
    return json.dumps(most_used_glass)


@app.route('/categories_by_average_number_of_ingredients')
def get_categories_by_average_number_of_ingredients():
    if 'categories' not in request.args:
        return
    categories = request.args.get('categories')
    categories = json.loads(categories)
    categories_by_avg_ingredients = DBConnection.execute_query(
        queries.query_categories_by_average_number_of_ingredients(categories))
    categories_dict = {'categories': categories_by_avg_ingredients}
    return json.dumps(categories_dict)


@app.route('/easy_to_make_from_category')
def get_easy_to_make_from_category():
    if ('cocktail_categoris' not in request.args) or ('meal_categories' not in request.args):
        return
    cocktail_categories = request.args.get('cocktail_categories')
    meal_categories = request.args.get('meal_categories')
    glass_categories = DBConnection.execute_query(queries.query_easy_to_make_from_category("Beef", "Shot"))
    return json.dumps('')


@app.route('/full_text_search')
def full_text_search():
    pass


@app.route('/common_ingredients')
def common_ingredients():
    pass


if __name__ == '__main__':
    app.run(debug=True, port="8000")
    app.run(threaded=True)  # GOOD YUVAL
