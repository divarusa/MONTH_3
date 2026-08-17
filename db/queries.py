CREATE_TABLE_USERS = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    phone TEXT NOT NULL
);
"""

INSERT_USER = """
INSERT INTO users (name, age, phone)
VALUES (?, ?, ?);
"""

SELECT_ALL_USERS = """
SELECT id, name, age, phone FROM users;
"""