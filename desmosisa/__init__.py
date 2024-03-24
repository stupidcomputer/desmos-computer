from .server import main
import argparse
import pyperclip
import json

def get_overrides(file):
    fd = open(file, "r")
    data = json.loads(fd.read())
    fd.close()
    return data

def define_args(parser):
    parser.add_argument('--copy', action="store_true", help="copy the client side JS to clipboard")
    parser.add_argument('--assemble', nargs=2, help="assemble the file INFILE and write the resultant overrides to OUTFILE")
    parser.add_argument('--run', help="specify file to start the desmos server for")
    parser.add_argument('--overrides', help="specify file that contains overrides for desmos expressions")


def entry():
    parser = argparse.ArgumentParser(
        prog="desmosisa",
        description="a smörgåsbord of utilities for desmos, including some implementations of an desmos-based isa",
    )

    define_args(parser)

    args = parser.parse_args()
    if args.overrides:
        args.overrides = get_overrides(args.overrides)

    if args.run:
        main(args.run, args.overrides if args.overrides else {})
    elif args.copy:
        fd = open("console.js", "r")
        buffer = fd.read()
        pyperclip.copy(buffer)
        print("copied")
    else:
        parser.print_help()

if __name__ == "__main__":
    entry()