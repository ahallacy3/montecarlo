from backend.helpers import get_db_connection

if __name__ == "__main__":
    conn, cur = get_db_connection()
    cur.execute("""CREATE TABLE IF NOT EXISTS price_in_usdt
    (timestamp timestamp, symbol text, price number)""")
