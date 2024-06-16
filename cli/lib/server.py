import asyncio
from websockets.server import serve
from websockets.sync.client import connect

import json
import random

class DesmosGraphServer:
    instructions_to_run = []
    outputs = []

    async def _reset(self, websocket):
        await websocket.send(
            json.dumps(
                {
                    "message": "clear",
                    "payload": "none",
                }
            )
        )

    async def _send_graph(self, websocket, graph):
        for line in graph.ast:
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
            else:
                # else just choose a safe option
                ident = "placeholder" + str(random.randint(1, 100100))

            await websocket.send(
                json.dumps(
                    {
                        "message": "expression",
                        "id": ident,
                        "payload": line.latex,
                    }
                )
            )

    async def _check_for_thing(self, websocket, expectedOutput, expression):
        await websocket.send(
            json.dumps(
                {
                    "message": "eval",
                    "expectedOutput": expectedOutput,
                    "expression": expression,
                }
            )
        )

    async def ws_main(self, websocket):
        message = await websocket.recv() # eat the client ping

        for instruction in self.instructions_to_run:
            await self._reset(websocket)

            if instruction["type"] == "insert_graph":
                await self._send_graph(websocket, instruction["graph"])

            elif instruction["type"] == "test_graph":
                await self._send_graph(websocket, instruction["graph"])
                await self._check_for_thing(
                    websocket,
                    instruction["expectedOutput"],
                    instruction["expression"]
                )

                message = await websocket.recv()
                jsonified = json.loads(message)
                result = jsonified["output"]
                self.outputs.append(
                    {
                        "name": instruction["name"],
                        "output": result,
                    }
                )

        self.stop.set_result("sotp please!!!!")

    async def main(self, stop):
        async with serve(self.ws_main, "localhost", 8764):
            self.stop = stop
            await stop

    def start(self):
        loop = asyncio.get_event_loop()
        stop = loop.create_future()

        loop.run_until_complete(self.main(stop))

    def append_inst(self, inst):
        self.instructions_to_run.append(inst)
