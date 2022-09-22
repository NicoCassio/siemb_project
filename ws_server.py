import asyncio
import json
import sqlite3
import websockets

CONNECTED = set()

DATABASE = 'access.db'
CON = sqlite3.connect(DATABASE)
CON.execute('PRAGMA foreign_keys = ON')
CUR = CON.cursor()

async def get_data():
    event = {
            'users': [],
            'logs': []
            }

    query = 'SELECT users.id, name, code FROM users INNER JOIN codes ON users.id = user_id'
    CUR.execute(query)
    users = CUR.fetchall()
    for user in users:
        event['users'].append({
            'id': user[0],
            'name': user[1],
            'code': user[2],
            })

    query = """ SELECT date(replace(datetime, "/", "-")), time(replace(datetime, "/", "-")), name FROM logs
                INNER JOIN users ON user_id = users.id """
    CUR.execute(query)
    logs = CUR.fetchall()
    for log in logs:
        event['logs'].append({
            'date': log[0],
            'time': log[1],
            'name': log[2],
            })
    return event

async def handler(websocket):
    async for message in websocket:
        CONNECTED.add(websocket)

        event = json.loads(message)
        print(event)
        if event['type'] == 'init':
            event = await get_data()
            await websocket.send(json.dumps(event))
        elif event['type'] == 'add':
            user = event['user']

            query = 'INSERT INTO users(name) VALUES (?)'
            CUR.execute(query, (user['name'].lower(),))
            CON.commit()

            query = 'INSERT INTO codes(code, user_id) SELECT ?, id FROM users WHERE name = ?'
            CUR.execute(query, (user['code'],user['name'].lower()))
            CON.commit()

            event = await get_data()
            print(len(CONNECTED))
            websockets.broadcast(CONNECTED, json.dumps(event))
        elif event['type'] == 'delete':
            user_id = event['user']['id']

            query = 'DELETE FROM users WHERE id = ?'
            CUR.execute(query, (user_id,))
            CON.commit()

            event = await get_data()
            print(len(CONNECTED))
            websockets.broadcast(CONNECTED, json.dumps(event))
        elif event['type'] == 'edit':
            user = event['user']

            query = 'UPDATE users SET name = ? WHERE id = ?'
            CUR.execute(query, (user['name'].lower(), user['id']))
            CON.commit()

            query = 'UPDATE codes SET code = ? WHERE user_id = ?'
            CUR.execute(query, (user['code'], user['id']))
            CON.commit()

            event = await get_data()
            print(len(CONNECTED))
            websockets.broadcast(CONNECTED, json.dumps(event))
        elif event['type'] == 'update':
            event = await get_data()
            print(len(CONNECTED))
            websockets.broadcast(CONNECTED, json.dumps(event))
    CONNECTED.remove(websocket)

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
