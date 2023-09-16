CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

CREATE TABLE chats (
    id SERIAL PRIMARY KEY,
    user1_id INTEGER REFERENCES users(id) NOT NULL,
    user2_id INTEGER REFERENCES users(id) NOT NULL
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    chat_id INTEGER REFERENCES chats(id) NOT NULL,
    sender_id INTEGER REFERENCES users(id) NOT NULL,
    message_text TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE languages (
    id SERIAL PRIMARY KEY,
    language_name VARCHAR(255) NOT NULL,
    native_name VARCHAR(255) NOT NULL,
    iso_639_1_code CHAR(2) NOT NULL
);

CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    user_id INT NOT NULL UNIQUE,
    languages_known JSONB,
    language_levels JSONB,
    bio TEXT,
    profile_color VARCHAR(7)
);