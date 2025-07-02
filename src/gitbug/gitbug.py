import os
import json
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

def get_coursespec():
    coursespec_file = open(coursespec_path,"r")
    coursespec = coursespec_file.read()
    coursespec_file.close()
    return json.loads(coursespec)

def update(critical=False):
    
    print("Updating coursespec...")
    response = requests.get(coursespec_url)

    try:
        response.raise_for_status()
        content = response.text

        with open(coursespec_path,"w") as file:
            file.write(content)
            file.close()

    except Exception as e:
        print("Error downloading coursespec. Using local copy.")

        if critical:
            print("FATAL: No local copy. Please connect to the internet to automatically download the coursespec.")

def clone_down(repo_id : str, assignment_id: str, output_path: str, coursespec):
    clone_location = os.path.join(output_path, repo_id)

    if (os.path.exists(clone_location)):
        print(f"FATAL: {repo_id} folder already exits in specified output path.")
        exit()

    os.mkdir(clone_location)
    print(coursespec)
    

def main():
    args = vars(parse_args())
    check_file_structure()
    coursespec = get_coursespec()
    clone_down(args["<repo-id>"], args["<assignment-id>"], args["output-path"], coursespec)

if __name__ == "__main__":
    main()
    