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
