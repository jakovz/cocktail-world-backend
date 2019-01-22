CREATE TABLE `meals` (
	`id` INT(5) NOT NULL,
	`name` VARCHAR(70) NOT NULL,
	`category` VARCHAR(50) NOT NULL,
	`area` VARCHAR(50) NULL DEFAULT NULL,
	`instructions` VARCHAR(10000) NOT NULL,
	`meal_img_url` VARCHAR(2083) NULL DEFAULT NULL,
	`tags` VARCHAR(500) NULL DEFAULT NULL,
	`youtube_video_url` VARCHAR(2083) NULL DEFAULT NULL,
	PRIMARY KEY (`id`),
	INDEX `mealsLengthInstractionsIndex` (`instructions`(500)),
	INDEX `mealsCategoryIndex` (`category`),
	FULLTEXT INDEX `instructions` (`instructions`),
	CONSTRAINT `FK_meals_food_categories` FOREIGN KEY (`category`) REFERENCES `food_categories` (`name`)
)
