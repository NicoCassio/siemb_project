import logging
import sqlite3
import sys
import time
import ws_client

def handle_unhandled_exceptions(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.critical('Unhandled exception', exc_info=(exc_type, exc_value, exc_traceback))
    logging.info('END')

def has_permission(code=None):
    DATABASE = 'access.db'
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    query = 'SELECT code FROM codes'
    cur.execute(query)
    res = cur.fetchall()

    codes = []
    for row in res:
        codes.append(row[0])

    if code in codes:
        access_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())

        query = 'SELECT name FROM users INNER JOIN codes ON users.id = codes.user_id WHERE code = ?'
        cur.execute(query, (code,))
        res = cur.fetchone()

        name = None
        if res:
            for row in res:
                name = res[0]
            logging.info(f'{name} entered')

        query = 'INSERT INTO logs(user_id, datetime) SELECT user_id, ? FROM codes WHERE code = ?'
        cur.execute(query, (access_time, code))
        con.commit()

        ws_client.main()

        return True

def main():
    has_permission(code='taasdeste')


if __name__ == '__main__':
    main()
