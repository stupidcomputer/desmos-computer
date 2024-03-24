from websockets.server import serve
import asyncio
import os
import time
import json
import random
import queue
import functools
from .parser import Parser, Statement
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileModifiedEvent
from watchdog.observers import Observer

class FSEHandler(FileSystemEventHandler):
    def __init__(self, queue, *args, **kwargs):
        self.queue = queue
        super().__init__(*args, **kwargs)

    def on_modified(self, event):
        self.queue.put("")

async def serv(websocket, file, overrides={}):
    message = await websocket.recv()
    lmtime = 0
    epsilon = 0.25 # tweak this to what makes sense. 0.25 seconds makes sense to me.
    q = queue.Queue()

    # make it read the file initially
    q.put("")

    # setup the watchdog
    observer = Observer()
    event_handler = FSEHandler(q)
    observer.schedule(event_handler, file)
    observer.start()

    print("client connected")

    while True:
        # there are sometimes multiple writes bundled close together -- so
        # debounce them.
        q.get()
        if time.time() - lmtime < epsilon:
            continue
        else:
            lmtime = time.time()

        parser = Parser(file)
        parser.parse()

        await websocket.send(
            json.dumps(
                {
                    "message": "clear",
                    "payload": "none",
                }
            )
        )

        for line in parser.ast:
            if line["ticker"]:
                await websocket.send(
                    json.dumps(
                        {
                            "message": "ticker",
                            "rate": line.commands["ticker"],
                            "payload": line.latex,
                        }
                    )
                )

                continue

            # if the line has been assigned an id, make it so
            if line["id"]:
                ident = line.commands["id"]
                print("performing substitution")
            else:
                # else just choose a safe option
                ident = "placeholder" + str(random.randint(1, 100100))

            if ident in overrides.keys():
                to_send = overrides[ident]
            else:
                to_send = line.latex


            await websocket.send(
                json.dumps(
                    {
                        "message": "expression",
                        "id": ident,
                        "payload": to_send,
                    }
                )
            )

async def start_server(file, overrides):
    print("starting server")
    wrapper = functools.partial(serv, file=file, overrides=overrides)
    async with serve(wrapper, "localhost", 8764):
        print("starting server for realz")
        await asyncio.Future()

def main(file, overrides):
    asyncio.run(start_server(file, overrides))

if __name__ == "__main__":
    main("data/testing.desmos")
