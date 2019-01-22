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


@app.route('/meal_categories')
def get_meal_categories():
    cocktail_categories = DBConnection.execute_query(queries.get_meal_categories())
    cocktail_categories = [category['category'] for category in json.loads(cocktail_categories)]
    categories_dict = {"allowed_meal_categories": cocktail_categories}
    return json.dumps(categories_dict)


@app.route('/drink')
def get_drink():
    if 'drink_name' not in request.args:
        return
    drink = request.args.get('drink_name')
    drink = json.loads(drink)
    drink = drink.encode('latin-1')
    drink_details = DBConnection.execute_query(queries.get_drink(drink))
    drink_details_dict = {"drink": drink_details}
    return json.dumps(drink_details_dict)


@app.route('/meal')
def get_meal():
    if 'meal_name' not in request.args:
        return
    meal = request.args.get('meal_name')
    meal = json.loads(meal)
    drink_details = DBConnection.execute_query(queries.get_meal(meal))
    drink_details_dict = {"meal": drink_details}
    return json.dumps(drink_details_dict)


@app.route('/glass_types')
def get_glass_categories():
    glass_categories = DBConnection.execute_query(queries.get_glasses_types())
    glass_categories = [category['glass_type'] for category in json.loads(glass_categories)]
    categories_dict = {"glass_types": glass_categories}
    return json.dumps(categories_dict)


@app.route('/calories_alcoholic')
def get_calories_alcoholic():
    # the key for the dictionary should be "drinks_meals"
    #  {"drinks_meals":[{"drink_name":"", "drink_img":"", "meal_name":"", "meal_img":""}, ... ]}
    if ('range_from' not in request.args) or ('range_to' not in request.args) or ('alcoholic' not in request.args):
        return
    range_from = request.args.get('range_from')
    range_to = request.args.get('range_to')
    alcoholic = request.args.get('alcoholic')
    range_from = json.loads(range_from)
    range_to = json.loads(range_to)
    alcoholic = json.loads(alcoholic)
    alcoholic = True if alcoholic == 'alcoholic' else False
    glass_categories = DBConnection.execute_query(
        queries.query_calories_alcoholic(range_from, range_to, alcoholic))
    glass_categories_dict = {'drinks': glass_categories}
    return json.dumps(glass_categories_dict)


@app.route('/cocktail_amount_by_glass_categories')
def get_cocktail_amount_by_glass_categories():
    if ('categories' not in request.args) or ('glass_type' not in request.args) or ('filter_type' not in request.args):
        return
    categories = request.args.get('categories')
    glass_type = request.args.get('glass_type')
    alcoholic = request.args.get('filter_type')
    categories = json.loads(categories)
    glass_type = json.loads(glass_type)
    alcoholic = json.loads(alcoholic)
    alcoholic = True if alcoholic == 'alcoholic' else False
    glass_categories = DBConnection.execute_query(
        queries.query_cocktail_amount_by_glass_categories(categories, alcoholic, glass_type))
    glass_categories_dict = {'categories_count': glass_categories}
    return json.dumps(glass_categories_dict)


@app.route('/ingredients_difference')
def get_ingredients_difference():
    if ('different_drinks' not in request.args) or ('ingredients_in_drink' not in request.args):
        return
    different_drinks = request.args.get('different_drinks')
    ingredients_in_drink = request.args.get('ingredients_in_drink')
    ingredients_difference = DBConnection.execute_query(
        queries.query_ingredients_difference(different_drinks, ingredients_in_drink))
    ingredients_difference_dict = {'ingredients': ingredients_difference}
    return json.dumps(ingredients_difference_dict)


@app.route('/most_used_non_alcoholic')
def get_most_used_non_alcoholic():
    most_used_glass_drinks = DBConnection.execute_query(queries.query_most_used_non_alcoholic())
    most_used_dict = {'drinks': most_used_glass_drinks, 'glass': json.loads(most_used_glass_drinks)[0]['glass_type']}
    return json.dumps(most_used_dict)


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
    if ('cocktail_categories' not in request.args) or ('meal_categories' not in request.args):
        return
    cocktail_categories = json.loads(request.args.get('cocktail_categories'))
    meal_categories = json.loads(request.args.get('meal_categories'))
    glass_categories = DBConnection.execute_query(
        queries.query_easy_to_make_from_category(meal_categories, cocktail_categories))
    glass_categories_dict = {'drinks_meals': glass_categories}
    return json.dumps(glass_categories_dict)


@app.route('/full_text_search')
def full_text_search():
    # to be completed
    if 'query' not in request.args:
        return
    query = json.loads(request.args.get('query'))
    query = DBConnection.execute_query(queries.query_full_text_search(query.split(' ')))
    full_search_dic = {'drinks': query}
    return json.dumps(full_search_dic)


@app.route('/common_ingredients')
def common_ingredients():
    if 'common_ingredients' not in request.args:
        return
    common_ingredients = json.loads(request.args.get('common_ingredients'))
    common_ingredients = DBConnection.execute_query(
        queries.query_common_ingredients(common_ingredients))
    common_ingredients_dict = {'common_ingredients': common_ingredients}
    return json.dumps(common_ingredients_dict)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="40875", debug=False, threaded=True)
