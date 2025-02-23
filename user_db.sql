CREATE DATABASE user_system;
USE user_system;
CREATE TABLE users(
	id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
INSERT INTO users (email, password) VALUES ('person@sample.com','password123');
