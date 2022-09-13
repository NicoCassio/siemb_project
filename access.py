import sqlite3
import time

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
            print(f'{name} entered')

        query = 'INSERT INTO logs(user_id, datetime) SELECT user_id, ? FROM codes WHERE code = ?'
        cur.execute(query, (access_time, code))
        con.commit()

        return True

def main():
    has_permission(code='taasdeste')


if __name__ == '__main__':
    main()
