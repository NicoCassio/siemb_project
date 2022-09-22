import gs
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

def main():
    now   = time.localtime()
    year  = now.tm_year
    month = now.tm_mon
    day   = now.tm_mday

    logging.basicConfig(filename=f'logs/{year}_{month}_{day}_update_db.log',
                        level=logging.DEBUG,
                        format='%(asctime)s - [%(levelname)s] %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S')

    sys.excepthook = handle_unhandled_exceptions

    logging.info('START')

    gs_data = gs.get_data()

    DATABASE = 'access.db'
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    query = 'SELECT * FROM users'
    cur.execute(query)
    res = cur.fetchall()
    db_users = {
        'ids': [],
        'names': []
    }
    for row in res:
        db_users['ids'].append(row[0])
        db_users['names'].append(row[1])

    query = """ SELECT codes.code, codes.user_id, users.name FROM codes
                    INNER JOIN users ON codes.user_id = users.id """
    cur.execute(query)
    res = cur.fetchall()
    db_codes = {
        'codes': [],
        'users_ids': [],
        'users_names': []
    }
    for row in res:
        db_codes['codes'].append(row[0])
        db_codes['users_ids'].append(row[1])
        db_codes['users_names'].append(row[2])

    new_names = []
    for gs_name in gs_data['names']:
        if gs_name not in db_users['names']:
            new_names.append((gs_name,))
    if new_names:
        query = 'INSERT INTO users(name) VALUES (?)'
        cur.executemany(query, new_names)
        con.commit()

    diff_codes = []
    new_codes = []
    for gs_code, gs_name in zip(gs_data['codes'], gs_data['names']):
        if gs_code not in db_codes['codes']:
            new_codes.append((gs_code, gs_name))
        else:
            db_code_index = db_codes['codes'].index(gs_code)
            if gs_name != db_codes['users_names'][db_code_index]:
                diff_codes.append((gs_name, gs_code))

    if diff_codes:
        query = """ UPDATE codes SET user_id = users.id
                        FROM (SELECT id FROM users WHERE name = ?) AS users WHERE code = ? """
        cur.executemany(query, diff_codes)
        con.commit()

    if new_codes:
        query = 'INSERT INTO codes(code, user_id) SELECT ?, users.id FROM users WHERE name = ?'
        cur.executemany(query, new_codes)
        con.commit()

    old_codes = []
    for db_code in db_codes['codes']:
        if db_code not in gs_data['codes']:
            old_codes.append((db_code,))

    if old_codes:
        query = 'DELETE FROM codes WHERE code = ?'
        cur.executemany(query, old_codes)
        con.commit()

    ws_client.main()

if __name__ == '__main__':
    main()
