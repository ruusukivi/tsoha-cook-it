CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    profilename TEXT NOT NULL UNIQUE,
    admin BOOLEAN DEFAULT FALSE
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
    created_at TIMESTAMP DEFAULT NOW(),
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    visible INTEGER NOT NULL
);

CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    liker_id INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    comment TEXT NOT NULL,
    author_id INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes,
    created_at TIMESTAMP DEFAULT NOW(),
    visible INTEGER NOT NULL
);

CREATE TABLE photos (
    id SERIAL PRIMARY KEY,
    name TEXT, 
    data BYTEA,
    size int,
    creator_id INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes,
    created_at TIMESTAMP DEFAULT NOW(),
    visible INTEGER NOT NULL
);

