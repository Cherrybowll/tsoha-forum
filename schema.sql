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
    name TEXT UNIQUE,
    limited_access BOOLEAN DEFAULT FALSE,
    visibility BOOLEAN DEFAULT TRUE
);

CREATE TABLE threads (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    subject TEXT,
    content TEXT,
    creator_id INT REFERENCES users,
    topic_id INT REFERENCES topics ON DELETE CASCADE,
    created_at TIMESTAMP
);

CREATE TABLE messages (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    content TEXT,
    creator_id INT REFERENCES users,
    thread_id INT REFERENCES threads ON DELETE CASCADE,
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

CREATE TABLE accesses (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id INT REFERENCES users,
    topic_id INT REFERENCES topics
);

INSERT INTO users (
    name,
    password,
    admin_role
) VALUES (
    'admin',
    'scrypt:32768:8:1$FJC1FTMn8BykRM3T$6e18c5b9ceb209e3647233c06088e423984b7c6544523d893134073fa9fcbe5ef582414f01bbcb0d2f035ef79ed0f67bed38fdb3a81c658e636f52c9d253af3b',
    TRUE
);
