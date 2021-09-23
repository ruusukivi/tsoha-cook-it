CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    profilename TEXT NOT NULL UNIQUE
);

CREATE TABLE types (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    typeid INTEGER REFERENCES types,
    description TEXT,
    steps TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    creator_id INTEGER REFERENCES users,
    created_at TIMESTAMP,
    visible INTEGER NOT NULL
);

