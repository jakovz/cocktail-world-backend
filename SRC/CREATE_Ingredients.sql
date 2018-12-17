CREATE TABLE `ingredients` (
	`id` INT(3) NOT NULL,
	`name` VARCHAR(50) NOT NULL,
	`description` VARCHAR(500) NOT NULL,
	`type` VARCHAR(50) NOT NULL,
	`ingredient_img_url` VARCHAR(2083) NOT NULL,
	`calories` INT(4) NOT NULL,
	PRIMARY KEY (`id`)
)
COMMENT='Ingredients:\r\na.	id (int (3))\r\nb.	name (string)\r\nc.	description (string)\r\nd.	type (string)\r\ne.	ingredient_img_url (string 2083 #as max length of url)\r\nf.	calories (int)'
COLLATE='utf8mb4_0900_ai_ci'
;
