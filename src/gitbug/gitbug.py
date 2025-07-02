import os
import requests
import hashlib
from argparse import ArgumentParser

gitbug_folder = os.path.expanduser("~/.gitbug")
coursespec_path = os.path.expanduser("~/.gitbug/coursespec.json")
coursespec_url = "https://raw.githubusercontent.com/chemicaldawn/cs61b-cli/refs/heads/main/resources/coursespec.json"

def parse_args():
    parser = ArgumentParser(
        prog = "gitbug",
        description = "",
    )
    parser.add_argument("<repo-id>")
    parser.add_argument("<assignment-id>")
    parser.add_argument("output-path", nargs="?", default="./")
    parser.add_argument("-u")
    return parser.parse_args()

def check_file_structure():
    if not os.path.exists(gitbug_folder):
        print("Creating gitbug cache directory...")
        os.mkdir(gitbug_folder)

    if not os.path.exists(coursespec_path):
        update(True)

def update(critical=False):
    
    print("Updating coursespec...")
    response = requests.get(coursespec_url)

    try:
        response.raise_for_status()
        content = response.text
    except:
        print("Error downloading coursespec. Using local copy.")

        if critical:
            print("FATAL: No local copy. Please connect to the internet to automatically download the coursespec.")

def main():
    args = parse_args()
    check_file_structure()

if __name__ == "__main__":
    main()
    