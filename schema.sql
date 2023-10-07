CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

CREATE TABLE chats (
    id SERIAL PRIMARY KEY,
    user1_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    user2_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    chat_id INTEGER REFERENCES chats(id) ON DELETE CASCADE NOT NULL,
    sender_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    message_text TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE languages (
    id SERIAL PRIMARY KEY,
    language_name VARCHAR(255) NOT NULL,
    native_name VARCHAR(255) NOT NULL,
    iso_639_1_code CHAR(2) NOT NULL
);

CREATE TABLE language_levels (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    language_id INTEGER REFERENCES languages(id) ON DELETE CASCADE,
    proficiency_level VARCHAR(255) NOT NULL,
    UNIQUE (user_id, language_id)
);

CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    bio TEXT,
    profile_color VARCHAR(7),
    image_data BYTEA
);

CREATE TABLE language_partners (
    id SERIAL PRIMARY KEY,
    user_id1 INT REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    user_id2 INT REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    request_status VARCHAR(20),
    request_message TEXT
);

CREATE TABLE community_posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE post_comments (
    id SERIAL PRIMARY KEY,
    post_id INT REFERENCES community_posts(id) ON DELETE CASCADE,
    author_id INT REFERENCES users(id) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    content TEXT
);
