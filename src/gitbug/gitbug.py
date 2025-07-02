import os
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(
        prog = "gitbug",
        description = "",
    )
    parser.add_argument("<repo-id>")
    parser.add_argument("<assignment-id>")
    parser.add_argument("output-path", nargs="?", default="./")
    return parser.parse_args()

def auto_update():
    if not os.path.exists("~/.gitbug/"):
        os.mkdir("~/.gitbug/")

    if not os.file.exists("~/.gitbug/coursemap.json")

def main():
    
    print(args)

if __name__ == "__main__":
    main()
    