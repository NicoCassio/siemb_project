import asyncio
import json
import sqlite3
import websockets

DATABASE = 'access.db'
CON = sqlite3.connect(DATABASE)
CUR = CON.cursor()

async def handler(websocket):
    async for message in websocket:
        event = json.loads(message)
        print(event)
        if event['type'] == 'init':
            query = 'SELECT name, code FROM users INNER JOIN codes ON users.id = user_id'
            CUR.execute(query)
            users = CUR.fetchall()
            print(users)

            query = """ SELECT date(replace(datetime, "/", "-")), time(replace(datetime, "/", "-")), name FROM logs
                        INNER JOIN users ON user_id = users.id """
            CUR.execute(query)
            logs = CUR.fetchall()

            event = {
                    'users': users,
                    'logs': logs
                    }
            await websocket.send(json.dumps(event))
        elif event['type'] == 'edit':
            print(event['user'])
            pass
        elif event['type'] == 'update':
            pass

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
