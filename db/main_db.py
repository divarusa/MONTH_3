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
        cursor.execute(queries.CREATE_TABLE_USER_INFO)
        conn.commit()
    finally:
        conn.close()
    print("БД подключена!")


def save_user(data: dict) -> int:
    conn = sqlite3.connect(PATH_DB)
    try:
        cursor = conn.cursor()
        cursor.execute(
            queries.INSERT_USER,
            (data["name"], data["age"], data["phone"])
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def save_user_info(user_id: int, data: dict):
    conn = sqlite3.connect(PATH_DB)
    try:
        cursor = conn.cursor()
        cursor.execute(
            queries.INSERT_USER_INFO,
            (user_id, data["city"])
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


def get_all_users_with_info():
    conn = sqlite3.connect(PATH_DB)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute(queries.SELECT_ALL_USERS_JOIN)
        rows = cursor.fetchall()
    finally:
        conn.close()
    return rows