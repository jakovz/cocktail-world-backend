CREATE TABLE `cocktails_ingredients` (
	`cocktail_id` INT NOT NULL,
	`ingredient_id` INT NOT NULL,
	`measure` VARCHAR(50) NULL,
	PRIMARY KEY (`cocktail_id`, `ingredient_id`)
)
COMMENT='Cocktails_ingredients:\r\na.	cocktail_id\r\nb.	ingredient_id\r\nc.	measure (string)'
COLLATE='utf8mb4_0900_ai_ci'
;
