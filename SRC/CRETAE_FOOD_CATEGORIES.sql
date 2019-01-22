CREATE TABLE `food_categories` (
	`id` INT(3) NOT NULL,
	`name` VARCHAR(100) NOT NULL,
	`category_img_link` VARCHAR(2083) NULL DEFAULT NULL,
	`description` VARCHAR(5083) NULL DEFAULT NULL,
	PRIMARY KEY (`name`),
	UNIQUE INDEX `id` (`id`)
)
