CREATE DATABASE IF NOT EXISTS SyriaData;
USE SyriaData;

CREATE TABLE IF NOT EXISTS Governorate (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS City (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    governorate_id BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (governorate_id) REFERENCES Governorate(id) ON DELETE CASCADE,
    UNIQUE (name, governorate_id)
);

CREATE TABLE IF NOT EXISTS District (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city_id BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (city_id) REFERENCES City(id) ON DELETE CASCADE,
    UNIQUE (name, city_id)
);

CREATE TABLE IF NOT EXISTS Town (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    district_id BIGINT UNSIGNED NOT NULL,
    FOREIGN KEY (district_id) REFERENCES District(id) ON DELETE CASCADE,
    UNIQUE (name, district_id)
);

CREATE VIEW SyriaLocationView AS
SELECT 
    g.name AS Governorate, 
    c.name AS City, 
    d.name AS District, 
    t.name AS Town
FROM Town t
JOIN District d ON t.district_id = d.id
JOIN City c ON d.city_id = c.id
JOIN Governorate g ON c.governorate_id = g.id;
