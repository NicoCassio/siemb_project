import logging
import sqlite3
import sys
import time

def handle_unhandled_exceptions(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.critical('Unhandled exception', exc_info=(exc_type, exc_value, exc_traceback))
    logging.info('END')

def main():
    START_TIME = time.perf_counter()

    now   = time.localtime()
    year  = now.tm_year
    month = now.tm_mon
    day   = now.tm_mday

    logging.basicConfig(filename=f'logs/{year}_{month}_{day}_create_db.log',
                        level=logging.DEBUG,
                        format='%(asctime)s - [%(levelname)s] %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S')

    sys.excepthook = handle_unhandled_exceptions

    logging.info('START')
    
    DATABASE = 'access.db'

    con = sqlite3.connect(DATABASE)
    con.execute('PRAGMA foreign_keys = ON')

    end_time = time.perf_counter()
    elapsed_time = end_time - START_TIME
    logging.info(f'Connection with database {DATABASE} established ({elapsed_time})')

    cur = con.cursor()

    drop_table_users = 'DROP TABLE IF EXISTS users'
    drop_table_codes = 'DROP TABLE IF EXISTS codes'
    drop_table_logs = 'DROP TABLE IF EXISTS logs'

    create_table_users = """ CREATE TABLE IF NOT EXISTS users (
            id   INTEGER PRIMARY KEY,
            name TEXT    NOT NULL
            )"""
    create_table_codes = """ CREATE TABLE IF NOT EXISTS codes (
            id      INTEGER PRIMARY KEY,
            code    TEXT    UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
            )"""
    create_table_logs = """ CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY,
            user_id    INTEGER NOT NULL,
            datetime   TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
            )"""

    cur.execute(drop_table_users)
    cur.execute(drop_table_codes)
    cur.execute(drop_table_logs)
    con.commit()

    end_time = time.perf_counter()
    elapsed_time = end_time - START_TIME
    logging.info(f'Tables dropped ({elapsed_time})')

    cur.execute(create_table_users)
    cur.execute(create_table_codes)
    cur.execute(create_table_logs)
    con.commit()

    end_time = time.perf_counter()
    elapsed_time = end_time - START_TIME
    logging.info(f'Tabled created ({elapsed_time})')

    end_time = time.perf_counter()
    elapsed_time = end_time - START_TIME
    logging.info(f'END ({elapsed_time})')


if __name__ == '__main__':
    main()
