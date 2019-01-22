CREATE TABLE 'cocktails_ingredients' (
	'cocktail_id' INT(5) NOT NULL,
	'ingredient_name' VARCHAR(50) NOT NULL,
	'measure' VARCHAR(50) NULL DEFAULT NULL,
	PRIMARY KEY ('cocktail_id', 'ingredient_name'),
	INDEX 'cocktailsIngredientsIndex' ('ingredient_name'),
	CONSTRAINT 'cocktail_id' FOREIGN KEY ('cocktail_id') REFERENCES 'drinks' ('id')
);

CREATE TABLE 'drinks' (
	'id' INT(5) NOT NULL,
	'name' VARCHAR(100) NOT NULL,
	'category' VARCHAR(50) NOT NULL,
	'iba' VARCHAR(100) NULL DEFAULT NULL,
	'is_alcoholic' VARCHAR(100) NOT NULL,
	'glass_type' VARCHAR(100) NOT NULL,
	'instructions' VARCHAR(10000) NOT NULL,
	'drink_img_url' VARCHAR(2083) NULL DEFAULT NULL,
	PRIMARY KEY ('id'),
	INDEX 'drinksCategoryIndex' ('category'),
	INDEX 'glassTypeIndex' ('glass_type'),
	INDEX 'drinksLengthInstractionsIndex' ('instructions'(50)),
	FULLTEXT INDEX 'instructions' ('instructions')
);

CREATE TABLE 'food_categories' (
	'id' INT(3) NOT NULL,
	'name' VARCHAR(100) NOT NULL,
	'category_img_link' VARCHAR(2083) NULL DEFAULT NULL,
	'description' VARCHAR(5083) NULL DEFAULT NULL,
	PRIMARY KEY ('name'),
	UNIQUE INDEX 'id' ('id')
);

CREATE TABLE 'ingredients' (
	'ingredient_name' VARCHAR(50) NOT NULL,
	'description' VARCHAR(5000) NOT NULL,
	'type' VARCHAR(50) NOT NULL,
	'ingredient_img_url' VARCHAR(2083) NOT NULL,
	'calories' INT(4) UNSIGNED NULL DEFAULT NULL,
	PRIMARY KEY ('ingredient_name')
);

CREATE TABLE 'meals' (
	'id' INT(5) NOT NULL,
	'name' VARCHAR(70) NOT NULL,
	'category' VARCHAR(50) NOT NULL,
	'area' VARCHAR(50) NULL DEFAULT NULL,
	'instructions' VARCHAR(10000) NOT NULL,
	'meal_img_url' VARCHAR(2083) NULL DEFAULT NULL,
	'tags' VARCHAR(500) NULL DEFAULT NULL,
	'youtube_video_url' VARCHAR(2083) NULL DEFAULT NULL,
	PRIMARY KEY ('id'),
	INDEX 'mealsLengthInstractionsIndex' ('instructions'(500)),
	INDEX 'mealsCategoryIndex' ('category'),
	FULLTEXT INDEX 'instructions' ('instructions'),
	CONSTRAINT 'FK_meals_food_categories' FOREIGN KEY ('category') REFERENCES 'food_categories' ('name')
);

CREATE TABLE 'meal_ingredients' (
	'meal_id' INT(5) NOT NULL,
	'ingredient_name' VARCHAR(50) NOT NULL,
	'measure' VARCHAR(50) NULL DEFAULT NULL,
	PRIMARY KEY ('meal_id', 'ingredient_name'),
	INDEX 'mealIngredientsIndex' ('ingredient_name'),
	CONSTRAINT 'meal_id' FOREIGN KEY ('meal_id') REFERENCES 'meals' ('id')
);
