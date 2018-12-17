CREATE TABLE `meals` (
	`id` INT NULL,
	`name` VARCHAR(50) NULL,
	`category` VARCHAR(50) NULL,
	`description` VARCHAR(250) NULL,
	`area` VARCHAR(50) NULL,
	`instructions` VARCHAR(500) NULL,
	`meal_img_url` VARCHAR(2083) NULL,
	`tags` VARCHAR(500) NULL,
	`youtube_video_url` VARCHAR(2083) NULL
)
COMMENT='Meals:\r\na.	Id\r\nb.	Name\r\nc.	category\r\nd.	description\r\ne.	area\r\nf.	instructions\r\ng.	meal_img_url\r\nh.	tags (maybe should change the type)\r\ni.	youtube_link'
COLLATE='utf8mb4_0900_ai_ci'
;
