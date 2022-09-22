import asyncio
import json
import websockets

async def send_update():
    async with websockets.connect('ws://localhost:8001') as websocket:
        event = {'type': 'update'}
        await websocket.send(json.dumps(event))

def main():
    asyncio.run(send_update())


if __name__ == '__main__':
    main()
