#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets

import dodecahedron


MODEL = {"value": 0}

USERS = set()


def model():
    geometry = dodecahedron.Dodecahedron(30)
    MODEL["value"] = geometry.tolist()
    return json.dumps({"type": "model", **MODEL})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(model())
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "minus":
                MODEL["value"] -= 1
                await notify_state()
            elif data["action"] == "plus":
                MODEL["value"] += 1
                await notify_state()
            else:
                logging.error("Unsupported event: {}", data)
    finally:
        await unregister(websocket)

def run(port=6789):
    logging.basicConfig()

    start_server = websockets.serve(counter, "localhost", port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
