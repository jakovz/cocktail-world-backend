CREATE TABLE `ingredients` (
	`ingredient_name` VARCHAR(50) NOT NULL,
	`description` VARCHAR(5000) NOT NULL,
	`type` VARCHAR(50) NOT NULL,
	`ingredient_img_url` VARCHAR(2083) NOT NULL,
	`calories` INT(4) UNSIGNED NULL DEFAULT NULL,
	PRIMARY KEY (`ingredient_name`)
)