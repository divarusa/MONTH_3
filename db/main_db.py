import os
import sqlite3
from db import queries

PATH_DB = os.path.join(os.path.dirname(__file__), "sqlite3.db")


def create_table():
    os.makedirs(os.path.dirname(PATH_DB), exist_ok=True)
    conn = sqlite3.connect(PATH_DB)
    try:
        cursor = conn.cursor()
        cursor.execute(queries.CREATE_TABLE_USERS)
        conn.commit()
    finally:
        conn.close()
    print("БД подключена!")


def save_user(data: dict):
    conn = sqlite3.connect(PATH_DB)
    try:
        cursor = conn.cursor()
        cursor.execute(
            queries.INSERT_USER,
            (data["name"], data["age"], data["phone"])
        )
        conn.commit()
    finally:
        conn.close()


def get_all_users():
    conn = sqlite3.connect(PATH_DB)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute(queries.SELECT_ALL_USERS)
        rows = cursor.fetchall()
    finally:
        conn.close()
    return rows