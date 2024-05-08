DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS refresh_tokens;
DROP TABLE IF EXISTS secrets;
DROP TABLE IF EXISTS csrf_tokens;

CREATE TABLE users (
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE refresh_tokens (
    username TEXT UNIQUE NOT NULL,
    token TEXT UNIQUE NOT NULL,
    expiry TIMESTAMP NOT NULL,
    old_tokens TEXT
);

CREATE TABLE csrf_tokens (
    username TEXT UNIQUE NOT NULL,
    token TEXT UNIQUE NOT NULL
);

CREATE TABLE secrets (
    username TEXT UNIQUE NOT NULL,
    secret TEXT NOT NULL
);