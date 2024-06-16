from .lib.server import DesmosGraphServer
from .lib.graphparser import DesmosGraph, DesmosGraphOverride

from .lib.clientside import payload as JSGraphPayload
from .tests.isa import test_entry_point

def main():
#    graph = DesmosGraph.from_file("data/computer.desmos")
#    override = DesmosGraphOverride.from_file("test.override")
#
#    graph.include_override(override)
#    server = DesmosGraphServer()
#    server.append_inst({
#        "type": "insert_graph",
#        "graph": graph,
#    })
#    server.append_inst({
#        "type": "test_graph",
#        "graph": graph,
#        "name": "test and assert addition",
#        "expectedOutput": [1, 4, 6, 0, 0, 4],
#        "expression": "B",
#    })
#    server.start()
#    print(server.outputs)
#
    test_entry_point()

if __name__ == "__main__":
    main()
