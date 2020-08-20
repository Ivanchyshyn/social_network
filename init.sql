CREATE USER social_user with encrypted password 'social_user';
CREATE DATABASE social;
GRANT ALL PRIVILEGES ON DATABASE social TO social_user;
