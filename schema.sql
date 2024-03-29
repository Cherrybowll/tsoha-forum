CREATE TABLE users (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name TEXT UNIQUE,
    password TEXT,
    admin_role BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP,
    banned BOOLEAN DEFAULT FALSE
);

CREATE TABLE topics (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    topic TEXT,
    access_group INTEGER[],
    visibility BOOLEAN
);

CREATE TABLE threads (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    subject TEXT,
    creator_id INT REFERENCES users,
    topic_id INT REFERENCES topics,
    created_at TIMESTAMP
);

CREATE TABLE messages (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    content TEXT,
    creator_id INT REFERENCES users,
    thread_id INT REFERENCES threads,
    topic_id INT REFERENCES topics,
    created_at TIMESTAMP
);

CREATE TABLE friends (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user1 INT REFERENCES users,
    user2 INT REFERENCES users
);

CREATE TABLE blocks (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user1 INT REFERENCES users,
    user2 INT REFERENCES users
);

CREATE TABLE media (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name TEXT,
    data BYTEA
);
