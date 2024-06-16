import unittest
import timeout_decorator
import time

from cli.lib.server import DesmosGraphServer
from cli.lib.graphparser import DesmosGraph, DesmosGraphOverride
from cli.data.computer import payload as computer_graph_payload

def arr_to_override_text(arr):
    arr = [str(i) for i in arr]
    return "B = \\left[{}\\right]".format(
        ", ".join(arr)
    )

def instruction_test_helper(override_text, expected_output):
    graph = DesmosGraph(computer_graph_payload)
    override = DesmosGraphOverride({
        "testing": arr_to_override_text(override_text)
    })

    graph.include_override(override)

    server = DesmosGraphServer()
    server.instructions_to_run = []
    server.append_inst({
        "type": "test_graph",
        "graph": graph,
        "name": "",
        "expectedOutput": expected_output,
        "expression": "B",
    })
    server.start()

    time.sleep(1)
    return server.outputs[-1]["output"] == "true"

class ISATest(unittest.TestCase):
    def test_store_positive(self):
        self.assertTrue(
            instruction_test_helper(
                [1, 4, 6, 0, 0, 0], # store lit. 4 to address 6
                [1, 4, 6, 0, 0, 4]
            )
        )

    def test_addition(self):
        self.assertTrue(
            instruction_test_helper(
                [2, 1, 1, 5, 0], # add addresses 1 and 1 to cell 5
                [2, 1, 1, 5, 4]
            )
        )

    def test_subtraction(self):
        self.assertTrue(
            instruction_test_helper(
                [12, 1, 2, 5, 0], # 12 - 1 into cell 5
                [12, 1, 2, 5, 11]
            )
        )

    def test_multiplication(self):
        self.assertTrue(
            instruction_test_helper(
                [13, 1, 3, 5, 0], # 13 * 3
                [13, 1, 3, 5, 39],
            )
        )

    def test_division(self):
        self.assertTrue(
            instruction_test_helper(
                [14, 1, 6, 5, 0, 7], # 14 / 7
                [14, 1, 6, 5, 2, 7],
            )
        )

    def test_division_with_decimal(self):
        self.assertTrue(
            instruction_test_helper(
                [14, 1, 6, 5, 0, 4], # 14 / 4 = 3.5
                [14, 1, 6, 5, 3.5, 4],
            )
        )
