import sqlite3
import math

from backend.constants import DB_NAME
print(sqlite3.sqlite_version)


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.create_function('pow', 2, math.pow)
    cur = conn.cursor()
    return conn, cur