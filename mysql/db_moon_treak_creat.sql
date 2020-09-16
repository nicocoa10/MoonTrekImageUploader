
CREATE TABLE `info` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `img` longblob NOT NULL,
  `location` varchar(100) NOT NULL,
  `city` varchar(45) NOT NULL,
  `time` datetime NOT NULL,
  `camera_info` varchar(150) NOT NULL,
  `telescope_type` varchar(45) NOT NULL,
  `lens_type` varchar(45) NOT NULL,
  `filter` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `access_to_app` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
