from websockets.server import serve
import asyncio
import os
import time
import json
import random
import queue
import functools
from parser import Parser
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileModifiedEvent
from watchdog.observers import Observer

class FSEHandler(FileSystemEventHandler):
    def __init__(self, queue, *args, **kwargs):
        self.queue = queue
        super().__init__(*args, **kwargs)

    def on_modified(self, event):
        self.queue.put("")

async def serv(websocket, file):
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
                
            if not line["comment"]:
                await websocket.send(
                    json.dumps(
                        {
                            "message": "expression",
                            "id": "placeholder" + str(random.randint(1, 100100)),
                            "payload": line.latex,
                        }
                    )
                )
            
async def start_server(file):
    wrapper = functools.partial(serv, file=file)
    async with serve(wrapper, "localhost", 8765):
        await asyncio.Future()

def main(file):
    asyncio.run(start_server(file))

if __name__ == "__main__":
    main("data/testing.desmos")