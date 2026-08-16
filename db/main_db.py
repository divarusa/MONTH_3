import sqlite3
from db import queries

PATH_DB = "db/sqlite3.db"


def init_db():
    conn = sqlite3.connect(PATH_DB)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_TABLE_USERS)
    conn.commit()
    conn.close()
    print("БД подключена!")


def save_user(data: dict):
    conn = sqlite3.connect(PATH_DB)
    cursor = conn.cursor()
    cursor.execute(queries.INSERT_USER, (data["name"], data["age"], data["phone"]))
    conn.commit()
    conn.close()


def get_all_users():
    conn = sqlite3.connect(PATH_DB)
    cursor = conn.cursor()
    cursor.execute(queries.SELECT_ALL_USERS)
    rows = cursor.fetchall()
    conn.close()
    return rows