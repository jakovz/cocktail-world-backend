all_ingredient_names = "SELECT ingredients.name FROM ingredients"
all_cocktails = "SELECT * FROM drinks"


def get_cocktails_by_ingredients(ingredients):
    cocktails_by_ingredients = "SELECT DISTINCT drinks.name, drinks.drink_img_url " \
                               "FROM drinks, cocktails_ingredients,ingredients " \
                               "WHERE drinks.id=cocktails_ingredients.cocktail_id " \
                               "AND cocktails_ingredients.ingredient_id=ingredients.id "
    for ingredient in ingredients:
        cocktails_by_ingredients += "AND ingredients.name='%s' "
    return cocktails_by_ingredients


def get_cocktails_by_filters(filters):
    cocktails_by_filters = "SELECT drinks.name, drinks.drink_img_url " \
                           "FROM (SELECT {min_max_none}(cocktail_ingredients.{filter_name}*cocktail_ingredients.measure)" \
                           "         ,drinks.id, drinks.name, drinks.drink_img_url)" \
                                    "FROM ingredients, cocktail_ingredients, drinks " \
                                    "WHERE ingredients.id=cocktail_ingredients.ingredient_id " \
                                    "AND drinks.id=cocktail_ingredients.cocktail_id" \
                                    "GROUP BY drinks.id)" \
                           "WHERE "
    for i, my_filter in enumerate(filters):
        filter_name = my_filter['filter_name']
        filter_type = my_filter['filter_type']
        if i != 0:
            cocktails_by_filters += "AND "
        if filter_type == "range":
            cocktails_by_filters.format(from_string="drinks, cocktails_ingredients, ingredients")
            cocktails_by_filters += "{0}<{1} AND {2}<{3}".format(my_filter['range'][0], filter_name, filter_name,
                                                                 my_filter['range'][1])
        elif filter_type == "min":
            cocktails_by_filters.format(min_max_none="min", filter_name=filter_name)
        else:
            cocktails_by_filters.format(
                from_string="(SELECT MAX(cocktail_ingredients.{0}*cocktail_ingredients.measure),drinks.id, "
                            "drinks.name, drinks.drink_img_url)" \
                            "FROM ingredients, cocktail_ingredients, drinks " \
                            "WHERE ingredients.id=cocktail_ingredients.ingredient_id " \
                            "AND drinks.id=cocktail_ingredients.cocktail_id" \
                            "GROUP BY drinks.id" \
                            ")".format(filter_name))
    return cocktails_by_filters


def get_ingredients_by_cocktails_commonness(cocktails_commonness, ingredient_commonness):
    return f"""SELECT DISTINCT ingredients.name, ingredients.ingredient_img_url
                FROM ingredients, (SELECT DISTINCT cocktails_ingredients.ingredient_name AS name
                FROM cocktails_ingredients
                WHERE cocktails_ingredients.cocktail_id IN (SELECT cocktail_view.id
                FROM (SELECT cocktails_ingredients.cocktail_id AS id, COUNT(*) AS count
                FROM cocktails_ingredients
                GROUP BY id
                HAVING count>={cocktails_commonness}) AS cocktail_view) AND
                cocktails_ingredients.ingredient_name IN (SELECT DISTINCT ingredient_view.name AS name
                FROM (SELECT cocktails_ingredients.ingredient_name AS name, COUNT(*) AS count
                FROM cocktails_ingredients
                GROUP BY name
                HAVING count>={ingredient_commonness}) AS ingredient_view)) AS T
                WHERE T.name=ingredients.name"""


def get_amount_per_categories(categories, alcoholic):
    categories_str = ""
    for i, category in enumerate(categories):
        if i != 0:
            categories_str += ", "
        categories_str += "\""+categories[i]+"\""

    alcoholic_str = "Alcoholic" if alcoholic else "Non alcoholic"
    return f"""SELECT drinks.category, count(*) as amount
                FROM drinks
                WHERE drinks.is_alcoholic = "{alcoholic_str}" AND
                        drinks.category IN ({categories_str})
                GROUP BY drinks.category
                ORDER BY amount 
                DESC"""


def get_drinks_categories():
    return "SELECT DISTINCT drinks.category FROM drinks"

def get_drinks_categories():
    return "SELECT DISTINCT meals.category FROM meals"s

def get_glasses_types():
    return "SELECT DISTINCT drinks.glass_type FROM drinks"






