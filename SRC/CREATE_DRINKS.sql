CREATE TABLE `drinks` (
	`id` INT(5) NOT NULL,
	`name` VARCHAR(100) NOT NULL,
	`category` VARCHAR(50) NOT NULL,
	`iba` VARCHAR(100) NULL DEFAULT NULL,
	`is_alcoholic` VARCHAR(100) NOT NULL,
	`glass_type` VARCHAR(100) NOT NULL,
	`instructions` VARCHAR(10000) NOT NULL,
	`drink_img_url` VARCHAR(2083) NULL DEFAULT NULL,
	PRIMARY KEY (`id`),
	INDEX `drinksCategoryIndex` (`category`),
	INDEX `glassTypeIndex` (`glass_type`),
	INDEX `drinksLengthInstractionsIndex` (`instructions`(50)),
	INDEX `mealsCategoryIndex` (`category`),
	FULLTEXT INDEX `instructions` (`instructions`)
)
