CREATE TABLE `meal_ingredients` (
	`meal_id` INT(5) NOT NULL,
	`ingredient_name` VARCHAR(50) NOT NULL,
	`measure` VARCHAR(50) NULL DEFAULT NULL,
	PRIMARY KEY (`meal_id`, `ingredient_name`),
	INDEX `mealIngredientsIndex` (`ingredient_name`)
)
