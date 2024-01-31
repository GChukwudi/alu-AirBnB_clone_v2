-- create database hbnb_test_db
-- create user hbnb_test with password hbnb_test_pwd in localhost
-- grant privileges to hbnb_test
-- grant select privileges on the database performance_schema to hbnb_test
-- flush privileges

CREATE DATABASE IF NOT EXISTS hbnb_test_db;
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;