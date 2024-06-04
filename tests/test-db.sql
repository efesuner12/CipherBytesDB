CREATE DATABASE test;

USE test;

CREATE TABLE `one` (
  `id` int NOT NULL AUTO_INCREMENT,
  `field` varchar(10) NOT NULL UNIQUE,
  `field_2` varchar(15),
  `field_3` varchar(20),
  `date_field` datetime DEFAULT CURRENT_TIMESTAMP,
  `chk_field` int,
  `test2_id` int,
  PRIMARY KEY (`id`),
  KEY `test2_id` (`test2_id`),
  CONSTRAINT `one_ibfk_1` FOREIGN KEY (`test2_id`) REFERENCES `two` (`id`),
  CONSTRAINT `CHK_field` CHECK ((`chk_field` > 0))
);

INSERT INTO `one` (`field`, `field_2`, `field_3`, `chk_field`, `test2_id`) VALUES ('test_1', 'test', 'test', 1, 2);
INSERT INTO `one` (`field`, `field_2`, `field_3`, `chk_field`) VALUES ('test_2', 'test', 'test', 1);
INSERT INTO `one` (`field`, `field_2`, `field_3`, `chk_field`) VALUES ('test_3', 'test', 'test', 1);
INSERT INTO `one` (`field`, `field_2`, `field_3`, `chk_field`) VALUES ('test_4', 'test', 'test', 1);
INSERT INTO `one` (`field`, `field_2`, `field_3`, `chk_field`) VALUES ('test_5', 'test', 'test', 1);
INSERT INTO `one` (`field`, `field_2`, `field_3`, `chk_field`) VALUES ('test_6', 'test', 'test', 1);
INSERT INTO `one` (`field`, `field_2`, `field_3`, `chk_field`) VALUES ('test_7', 'test', 'test', 1);
INSERT INTO `one` (`field`, `field_2`, `field_3`, `chk_field`) VALUES ('test_8', 'test', 'test', 1);
INSERT INTO `one` (`field`, `field_2`, `field_3`, `chk_field`) VALUES ('test_9', 'test', 'test', 1);
INSERT INTO `one` (`field`, `field_2`, `field_3`, `chk_field`) VALUES ('test_10', 'test', 'test', 1);

SELECT * FROM one;

DESCRIBE one;

CREATE TABLE `two` (
  `id` int NOT NULL AUTO_INCREMENT,
  `field` varchar(255),
  `date_field` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

INSERT INTO two (id, field) VALUES (2, '11111111111111111111111111111111111111111');

SELECT * FROM two;

DESCRIBE two;
