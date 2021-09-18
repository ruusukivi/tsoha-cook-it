CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    profilename TEXT NOT NULL UNIQUE
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name TEXT  NOT NULL,
    description TEXT,
    creator_id INTEGER  NOT NULL REFERENCES users,
    created_at TIMESTAMP
);
