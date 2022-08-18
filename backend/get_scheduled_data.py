import schedule
import time
import requests

from multiprocessing import Pool

from backend.constants import DATA_URL, CRYPTO_SYMBOLS, BASE_SYMBOL
from backend.helpers import get_db_connection


def get_one_symbol(symbol, base):
    x = requests.get(DATA_URL.format(symbol + base))
    conn, cur = get_db_connection()
    cur.execute(f"INSERT INTO price_in_usdt (timestamp, symbol, price) VALUES (datetime(), '{symbol + base}', {x.json()['result']['price']})")
    conn.commit()

def get_new_data():
    with Pool(len(CRYPTO_SYMBOLS)) as p:
        p.starmap(get_one_symbol, [(symbol, BASE_SYMBOL) for symbol in CRYPTO_SYMBOLS])

if __name__ == "__main__":
    get_new_data()
    schedule.every(1).minute.do(get_new_data)

    while True:
        schedule.run_pending()
        time.sleep(1)