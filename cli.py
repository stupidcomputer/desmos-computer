from server import main
import argparse

def entry():
    parser = argparse.ArgumentParser(
        prog="desmos-sync",
        description="Synchronize from local file to Desmos calculator",
    )

    parser.add_argument("filename")
    args = parser.parse_args()
    main(args.filename)

if __name__ == "__main__":
    entry()