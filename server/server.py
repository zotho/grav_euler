#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import time

import dodecahedron

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

MODEL = {"value": list()}

ROTATION = {"value": None, "rotation_time": 0., "last_rotation_user": None}

AVAILABLE_USER_NUMBERS = list(range(9))
USER_NUMBER_MAPPING = dict()
USERS = set()


def model():
    geometry = dodecahedron.Dodecahedron(30)
    MODEL["value"] = geometry.tolist()
    return json.dumps({"type": "model", **MODEL})


def rotate():
    return json.dumps({"type": "rotate", **{key: ROTATION[key] for key in ["value", "rotation_time"]}})


def users_event():
    return json.dumps({"type": "users", "value": list(USER_NUMBER_MAPPING.values())})


async def notify_model():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = model()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_rotate(last_user):
    other_users = {user for user in USERS if user is not last_user}
    if other_users and ROTATION.get("value"):  # asyncio.wait doesn't accept an empty list
        message = rotate()
        await asyncio.wait([user.send(message) for user in other_users])


async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    logger.info("Register")
    USERS.add(websocket)
    USER_NUMBER_MAPPING[websocket] = AVAILABLE_USER_NUMBERS.pop(0)
    await notify_users()
    if ROTATION.get("value"):
        await asyncio.wait([websocket.send(rotate())])


async def unregister(websocket):
    logger.info("Unregister")
    USERS.remove(websocket)
    await notify_users()


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await notify_model()
        # await     websocket.send(model())
        async for message in websocket:
            data = json.loads(message)
            # if data["action"] == "minus":
            #     MODEL["value"] -= 1
            #     await notify_model()
            # elif data["action"] == "plus":
            #     MODEL["value"] += 1
            #     await notify_model()
            if data["action"] == "rotate":
                logger.info("Rotation")
                ROTATION["value"] = data["value"]
                ROTATION["rotation_time"] = time.time()
                ROTATION["last_rotation_user"] = websocket
                await notify_rotate(websocket)
            else:
                logger.error("Unsupported event: {}", data)
    finally:
        await unregister(websocket)


def run(port=6789):
    logger.info("Starting websocket server")
    start_server = websockets.serve(counter, "localhost", port)
    logger.info("Websocket server started")

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
