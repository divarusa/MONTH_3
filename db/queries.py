CREATE_TABLE_USERS = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    phone TEXT NOT NULL,
    photo_id TEXT
);
"""

CREATE_TABLE_USER_INFO = """
CREATE TABLE IF NOT EXISTS user_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    city TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
"""

INSERT_USER = """
INSERT INTO users (name, age, phone, photo_id)
VALUES (?, ?, ?, ?);
"""

INSERT_USER_INFO = """
INSERT INTO user_info (user_id, city)
VALUES (?, ?);
"""

SELECT_ALL_USERS = """
SELECT id, name, age, phone, photo_id FROM users;
"""

SELECT_ALL_USERS_JOIN = """
SELECT users.id, users.name, users.age, users.phone, users.photo_id, user_info.city
FROM users
INNER JOIN user_info ON users.id = user_info.user_id;
"""
