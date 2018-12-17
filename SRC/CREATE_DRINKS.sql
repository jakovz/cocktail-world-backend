CREATE TABLE `drinks` (
	`id` INT(5) NOT NULL,
	`name` VARCHAR(100) NOT NULL,
	`instructions` VARCHAR(500) NOT NULL,
	`category` VARCHAR(50) NOT NULL,
	`iba` VARCHAR(100) NOT NULL,
	`is_alcoholic` VARCHAR(100) NOT NULL,
	`glass_type` VARCHAR(100) NOT NULL,
	`drink_img_url` VARCHAR(2083) NOT NULL,
	PRIMARY KEY (`id`)
)
COMMENT='Drinks:\r\na.	id (int (5) primary_key)\r\nb.	name (string)\r\nc.	instructions (string)\r\nd.	category (string) (Maybe we need to restrict to the categories we have)\r\ne.	iba (string)\r\nf.	is_alcoholic (string)\r\ng.	glass_type (string)\r\nh.	drink_img_url (string)'
COLLATE='utf8mb4_0900_ai_ci'
;
