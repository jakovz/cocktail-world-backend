CREATE TABLE `cocktails_ingredients` (
	`cocktail_id` INT(5) NOT NULL,
	`ingredient_name` VARCHAR(50) NOT NULL,
	`measure` VARCHAR(50) NULL DEFAULT NULL,
	PRIMARY KEY (`cocktail_id`, `ingredient_name`),
	INDEX `cocktailsIngredientsIndex` (`ingredient_name`),
	CONSTRAINT `cocktail_id` FOREIGN KEY (`cocktail_id`) REFERENCES `drinks` (`id`)
)