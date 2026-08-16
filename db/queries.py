CREATE_TABLE_USERS = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    phone TEXT
);
"""

INSERT_USER = """
INSERT INTO users (name, age, phone)
VALUES (?, ?, ?);
"""

SELECT_ALL_USERS = """
SELECT name, age, phone FROM users;
"""