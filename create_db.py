import sqlite3

def main():
    DATABASE = 'access.db'

    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    drop_table_users = 'DROP TABLE IF EXISTS users'
    drop_table_codes = 'DROP TABLE IF EXISTS code'
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
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
            )"""

    cur.execute(drop_table_users)
    cur.execute(drop_table_codes)
    cur.execute(drop_table_logs)
    con.commit()

    cur.execute(create_table_users)
    cur.execute(create_table_codes)
    cur.execute(create_table_logs)
    con.commit()


if __name__ == '__main__':
    main()
