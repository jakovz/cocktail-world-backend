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
    ingredients_dict = {"ingredients": DBConnection.execute_query(queries.all_ingredients)}
    return json.dumps(ingredients_dict)


@app.route('/filters')
def get_available_filters():
    """
    :return: A json representing all the filters we support
    """
    # here should come a db query
    filters_dict = {"filters": AVAILABLE_FILTERS}
    return json.dumps(filters_dict)


def get_cocktails_by_ingredients(ingredients):
    return DBConnection.execute_query(queries.get_cocktails_by_ingredients(ingredients), *ingredients)


def get_cocktails_by_filters(filters):
    return DBConnection.execute_query(queries.get_cocktails_by_filters(filters))


def get_cocktails_by_filters_and_ingredients(filters, ingredients):
    pass


@app.route('/cocktails')
def get_cocktails():
    """
    The url is of the form:
    /cocktails?ingredient={"ingredients":[LIST_OF_INGREDIENTS]}&filter={"filters": [LIST_OF_FILTERS]}
    :return: json representing all matching cocktails
    """
    ingredients = None
    filters = None
    if len(request.args) == 0:
        return DBConnection.execute_query(queries.all_cocktails)
    if "ingredient" in request.args:
        ingredients = json.loads(request.args.get('ingredient'))['ingredients']
        print(ingredients)
    if "filter" in request.args:
        filters = json.loads(request.args.get('filter'))['filters']
        print(filters)
    if ingredients and not filters:
        cocktails = get_cocktails_by_ingredients(ingredients)
    elif filters and not ingredients:
        cocktails = get_cocktails_by_filters(filters)
    else:
        cocktails = get_cocktails_by_filters_and_ingredients(filters, ingredients)
    if cocktails is not None:
        return cocktails
    else:
        return "An error occurred during querying the DB."


if __name__ == '__main__':
    app.run(debug=True, port="8000")
    app.run(threaded=True)  # GOOD YUVAL
