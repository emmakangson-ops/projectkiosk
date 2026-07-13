--mysql -u root -p

-- create User
drop user if exists 'kiosk'@'localhost';
create user 'kiosk'@'localhost' IDENTIFIED BY 'kiosk1234';
create user 'kiosk'@'192.168.0.%' IDENTIFIED BY 'kiosk1234';
-- create Database
drop database if exists kiosk;
CREATE DATABASE kiosk;

-- grant CRUD
GRANT ALL PRIVILEGES ON kiosk.* to 'kiosk'@'localhost';
GRANT ALL PRIVILEGES ON kiosk.* to 'kiosk'@'192.168.0.%';

FLUSH PRIVILEGES;