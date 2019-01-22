all_ingredient_names = "SELECT ingredients.name FROM ingredients"
all_cocktails = "SELECT * FROM drinks"


def makes_str_list_for_query(list_to_str):
    str = ""
    for i, element in enumerate(list_to_str):
        if i != 0:
            str += ", "
        str += "\"" + list_to_str[i] + "\""
    return str


def get_meal(meal):
    return "SELECT * FROM meals WHERE meals.name=\"{meal}\"".format(meal=meal)


def get_drink(drink):
    return "SELECT * FROM drinks WHERE drinks.name=\"{drink}\"".format(drink=drink)


def get_cocktails_by_ingredients(ingredients):
    cocktails_by_ingredients = "SELECT DISTINCT drinks.name, drinks.drink_img_url " \
                               "FROM drinks, cocktails_ingredients,ingredients " \
                               "WHERE drinks.id=cocktails_ingredients.cocktail_id " \
                               "AND cocktails_ingredients.ingredient_id=ingredients.id "
    for ingredient in ingredients:
        cocktails_by_ingredients += "AND ingredients.name='%s' "
    return cocktails_by_ingredients


def query_ingredients_difference(cocktails_commonness, ingredient_commonness):
    return ("SELECT DISTINCT ingredients.ingredient_name, ingredients.ingredient_img_url " +
            "FROM ingredients, (SELECT DISTINCT cocktails_ingredients.ingredient_name AS name " +
            "FROM cocktails_ingredients " +
            "WHERE cocktails_ingredients.cocktail_id IN (SELECT cocktail_view.id " +
            "FROM (SELECT cocktails_ingredients.cocktail_id AS id, COUNT(*) AS count " +
            "FROM cocktails_ingredients " +
            "GROUP BY id " +
            "HAVING count>={cocktails_commonness}) AS cocktail_view) AND " +
            "cocktails_ingredients.ingredient_name IN (SELECT DISTINCT ingredient_view.name AS name " +
            "FROM (SELECT cocktails_ingredients.ingredient_name AS name, COUNT(*) AS count " +
            "FROM cocktails_ingredients " +
            "GROUP BY name " +
            "HAVING count>={ingredient_commonness}) AS ingredient_view)) AS T " +
            "WHERE T.name=ingredients.ingredient_name").format(cocktails_commonness=cocktails_commonness, ingredient_commonness=ingredient_commonness)


def query_most_used_non_alcoholic():
    return ("SELECT drinks.* " +
            "FROM drinks " +
            "WHERE drinks.glass_type = " +
            "(SELECT glasses.type " +
            "FROM (SELECT drinks.glass_type AS type, COUNT(*) AS count " +
            "FROM drinks " +
            "WHERE drinks.is_alcoholic = \"Non alcoholic\" AND " +
            "drinks.glass_type IN (SELECT drinks.glass_type " +
            "FROM drinks " +
            "WHERE drinks.is_alcoholic = \"Alcoholic\" " +
            "GROUP BY drinks.glass_type) " +
            "GROUP BY drinks.glass_type " +
            "ORDER BY count " +
            "DESC " +
            "LIMIT 1) AS glasses)")


def query_easy_to_make_from_category(food_category, drink_category):
    food_category_str = makes_str_list_for_query(food_category)
    drink_category_str = makes_str_list_for_query(drink_category)
    return ("SELECT drink_name, drink_img_url, meal_name, meal_img_url " +
            "FROM (SELECT drinks.name AS drink_name, drinks.drink_img_url " +
            "FROM drinks " +
            "WHERE LENGTH(drinks.instructions)<=50 " +
            "AND drinks.category IN ({drink_category_str})) AS T1, " +
            "(SELECT meals.name AS meal_name, meals.meal_img_url " +
            "FROM meals " +
            "WHERE LENGTH(meals.instructions)<=10000 " +
            "AND meals.category IN ({food_category_str})) AS T2").format(drink_category_str=drink_category_str,
                                                                         food_category_str=food_category_str)


def query_categories_by_average_number_of_ingredients(categories):
    categories_str = makes_str_list_for_query(categories)

    return ("SELECT drinks.category, AVG(T1.amount) as amount " +
            "FROM drinks, (SELECT cocktails_ingredients.cocktail_id AS id, COUNT(*) AS amount " +
            "FROM cocktails_ingredients " +
            "GROUP BY id) as T1 " +
            "WHERE T1.id = drinks.id AND " +
            "drinks.category IN ({categories_str}) " +
            "GROUP BY drinks.category " +
            "ORDER BY amount DESC").format(categories_str=categories_str)


def query_cocktail_amount_by_glass_categories(categories, alcoholic, glass_type):
    categories_str = makes_str_list_for_query(categories)

    alcoholic_str = "Alcoholic" if alcoholic else "Non alcoholic"
    return ("SELECT drinks.category, count(*) as amount " +
            "FROM drinks " +
            "WHERE drinks.is_alcoholic = \"{alcoholic_str}\" AND " +
            "drinks.category IN ({categories_str}) AND " +
            "drinks.glass_type = \"{glass_type}\" " +
            "GROUP BY drinks.category " +
            "ORDER BY amount " +
            "DESC").format(alcoholic_str=alcoholic_str, categories_str=categories_str, glass_type=glass_type)


def query_common_ingredients(common_ingredients):
    return ("SELECT drinks.name AS drink_name, drinks.drink_img_url, meals.name AS meal_name, meals.meal_img_url " +
            "FROM drinks, meals, (SELECT DISTINCT cocktails_ingredients.cocktail_id AS drink_id, " +
            "meal_ingredients.meal_id AS meal_id " +
            "FROM cocktails_ingredients, meal_ingredients " +
            "WHERE cocktails_ingredients.ingredient_name = meal_ingredients.ingredient_name " +
            "GROUP BY cocktails_ingredients.cocktail_id, meal_ingredients.meal_id " +
            "HAVING count(*) >= {common_ingredients}) as T1 " +
            "WHERE drinks.id = T1.drink_id AND meals.id = T1.meal_id").format(common_ingredients=common_ingredients)


def query_full_text_search(words_for_search):
    str = ""
    for i, word in enumerate(words_for_search):
        if i != 0:
            str += ", "
        str += word
    return ("SELECT name, img_url, instructions " +
            "FROM ((SELECT drinks.name, drinks.drink_img_url AS img_url, drinks.instructions " +
            "FROM drinks " +
            "WHERE MATCH(instructions) AGAINST('{str}')) " +
            "UNION " +
            "(SELECT meals.name, meals.meal_img_url AS img_url, meals.instructions " +
            "FROM meals " +
            "WHERE MATCH(instructions) AGAINST('{str}')) " +
            ") T_combine").format(str=str)


def query_ingredients_per_drink(name):
    return ("SELECT cocktails_ingredients.ingredient_name " +
            "FROM cocktails_ingredients " +
            "WHERE cocktails_ingredients.cocktail_id IN (SELECT drinks.id " +
            "FROM drinks " +
            "WHERE drinks.name = \"{name}\")").format(name=name)


def query_ingredients_per_meal(name):
    return ("SELECT meal_ingredients.ingredient_name " +
            "FROM meal_ingredients " +
            "WHERE meal_ingredients.meal_id IN (SELECT meals.id " +
            "FROM meals " +
            "WHERE meals.name = \"{name}\")").format(name=name)


def query_calories_alcoholic(range_from, range_to, alcoholic):
    alcoholic_str = "Alcoholic" if alcoholic else "Non alcoholic"
    return ("SELECT drinks.name AS drink_name, drinks.drink_img_url, meals.name AS meal_name, meals.meal_img_url " +
            "FROM drinks, meals, (SELECT cocktail_T.drink_id, meal_T.meal_id, " +
            "(cocktail_T.drink_cal + meal_T.meal_cal) AS total_cal " +
            "FROM(SELECT drinks.id AS drink_id, SUM(cocktails_ingredients.measure * ingredients.calories) AS drink_cal " +
            "FROM cocktails_ingredients, drinks, ingredients " +
            "WHERE drinks.is_alcoholic = \"{alcoholic_str}\" AND " +
            "drinks.id = cocktails_ingredients.cocktail_id AND " +
            "cocktails_ingredients.ingredient_name = ingredients.ingredient_name " +
            "GROUP BY drinks.id " +
            "HAVING SUM(cocktails_ingredients.measure * ingredients.calories) >= {range_from} AND " +
            "SUM(cocktails_ingredients.measure * ingredients.calories) <= {range_to}) AS cocktail_T, " +
            "(SELECT meals.id AS meal_id, SUM(meal_ingredients.measure * ingredients.calories) AS meal_cal " +
            "FROM meal_ingredients, meals, ingredients " +
            "WHERE meals.id = meal_ingredients.meal_id AND " +
            "meal_ingredients.ingredient_name = ingredients.ingredient_name " +
            "GROUP BY meals.id " +
            "HAVING SUM(meal_ingredients.measure * ingredients.calories) >= {range_from} AND " +
            "SUM(meal_ingredients.measure * ingredients.calories) <= {range_to})  AS meal_T " +
            "WHERE (cocktail_T.drink_cal + meal_T.meal_cal) >= {range_from} AND " +
            "(cocktail_T.drink_cal + meal_T.meal_cal) <= {range_to}) AS T_cal " +
            "WHERE T_cal.drink_id = drinks.id AND T_cal.meal_id = meals.id").format(alcoholic_str=alcoholic_str,
                                                                                    range_from=range_from,
                                                                                    range_to=range_to)


def get_drinks_categories():
    return "SELECT DISTINCT drinks.category FROM drinks"


def get_meal_categories():
    return "SELECT DISTINCT meals.category FROM meals"


def get_glasses_types():
    return "SELECT DISTINCT drinks.glass_type FROM drinks"


# SELECT DISTINCT cocktails_ingredients.ingredient_name
# FROM cocktails_ingredients
# WHERE cocktails_ingredients.cocktail_id = 11000
#
#
# SELECT DISTINCT meal_ingredients.ingredient_name
# FROM meal_ingredients
# WHERE meal_ingredients.meal_id = 52764