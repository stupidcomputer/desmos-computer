from .lib.server import DesmosGraphServer
from .lib.graphparser import DesmosGraph, DesmosGraphOverride

from .lib.clientside import payload as JSGraphPayload
from .data.computer import payload as ComputerPayload
from .data.testing import payload as TestingPayload

import pyperclip

import argparse

def handle_sync(parser):
    if parser.copy_userscript:
        pyperclip.copy(JSGraphPayload)
        print("copied userscript to clipboard")

    if parser.filename:
        graph = DesmosGraph.from_file(parser.filename)

        if parser.override:
            override = DesmosGraphOverride.from_file(parser.override)
            graph.include_override(override)

        server = DesmosGraphServer()
        server.instructions_to_run = []
        server.append_inst({
            "type": "insert_graph",
            "graph": graph,
        })
        server.start(no_stop=True)

def handle_data(parser):
    if parser.dataname:
        if parser.dataname == "computer.desmos":
            print(ComputerPayload)
        elif parser.dataname == "testing.desmos":
            print(TestingPayload)
        return

    if parser.list:
        parsers = ["computer.desmos", "testing.desmos"]
        print('\n'.join(parsers))

def main():
    parser = argparse.ArgumentParser(
        prog="desmosisa",
        description="a smörgåsbord of utilities for desmos, including some implementations of an desmos-based isa",
    )
    subparsers = parser.add_subparsers(dest="subparser_name")
    sync_parser = subparsers.add_parser("sync", help="desmos calculator synchronization utilities")
    sync_parser.add_argument(
        'filename',
        nargs='?',
        help="filename of DesmosExpressions to synchronize with client"
    )
    sync_parser.add_argument(
        '-o', '--override',
        help="filename of DesmosOverride file, to override certain expressions in the DesmosExpression file",
        action="store"
    )
    sync_parser.add_argument(
        '-c', '--copy-userscript',
        help="copy the userscript to the clipboard, to be pasted into the JS console within the calculator.",
        action="store_true"
    )

    data_parser = subparsers.add_parser("data", help="access various prebuilt files")
    data_parser.add_argument(
        'dataname',
        nargs='?',
        help='name of the datafile requested'
    )
    data_parser.add_argument(
        '-l', '--list',
        help='list available datafiles',
        action='store_true'
    )

    args = parser.parse_args()

    if args.subparser_name == "sync":
        handle_sync(args)
    if args.subparser_name == "data":
        handle_data(args)

if __name__ == "__main__":
    main()
