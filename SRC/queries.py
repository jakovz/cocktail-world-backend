all_ingredients = "SELECT * FROM ingredients"
all_cocktails = "SELECT * FROM drinks"


def get_cocktails_by_ingredients(ingredients):
    cocktails_by_ingredients = "SELECT DISTINCT drinks.name, drinks.drink_img_url " \
                               "FROM drinks, cocktails_ingredients,ingredients " \
                               "WHERE drinks.id=cocktails_ingredients.cocktail_id " \
                               "AND cocktails_ingredients.ingredient_id=ingredients.id "
    for ingredient in ingredients:
        cocktails_by_ingredients += "AND ingredients.name='%s' "
    return cocktails_by_ingredients
