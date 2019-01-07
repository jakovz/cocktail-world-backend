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


def query_ingredients_difference(cocktails_commonness, ingredient_commonness):
    return f"""SELECT DISTINCT ingredients.ingredient_name, ingredients.ingredient_img_url
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
                WHERE T.name=ingredients.ingredient_name"""


def query_most_used_non_alcoholic():
    return f"""SELECT drinks.*
            FROM drinks
            WHERE drinks.glass_type =
            (SELECT glasses.type
            FROM (SELECT drinks.glass_type AS type, COUNT(*) AS count
            FROM drinks
            WHERE drinks.is_alcoholic = "Non alcoholic" AND
            drinks.glass_type IN (SELECT drinks.glass_type
            FROM drinks
            WHERE drinks.is_alcoholic = "Alcoholic"
            GROUP BY drinks.glass_type)
            GROUP BY drinks.glass_type
            ORDER BY count
            DESC 
            LIMIT 1) AS glasses)"""


def query_easy_to_make_from_category(food_category, drink_category):
    return f"""SELECT *
                FROM (SELECT *
                FROM drinks
                WHERE LENGTH(drinks.instructions)<=50
                AND drinks.category = "{drink_category}") AS T1,
                (SELECT *
                FROM meals
                WHERE LENGTH(meals.instructions)<=10000
                AND meals.category = "{food_category}") AS T2
                """


def query_categories_by_average_number_of_ingredients(categories):
    categories_str = ""
    for i, category in enumerate(categories):
        if i != 0:
            categories_str += ", "
        categories_str += "\""+categories[i]+"\""

    return f"""SELECT drinks.category, AVG(T1.amount) as amount
                FROM drinks, (SELECT cocktails_ingredients.cocktail_id AS id, COUNT(*) AS amount
                FROM cocktails_ingredients
                GROUP BY id) as T1
                WHERE T1.id = drinks.id AND
                drinks.category IN ({categories_str})
                GROUP BY drinks.category 
                ORDER BY amount DESC"""


def query_cocktail_amount_by_glass_categories(categories, alcoholic):
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


def get_meal_categories():
    return "SELECT DISTINCT meals.category FROM meals"


def get_glasses_types():
    return "SELECT DISTINCT drinks.glass_type FROM drinks"






