import os
import stat
import json
import requests
import hashlib
from subprocess import run
from shutil import move, rmtree
from re import findall
from argparse import ArgumentParser

gitbug_folder = os.path.expanduser("~/.gitbug")
coursespec_path = os.path.expanduser("~/.gitbug/coursespec.json")
coursespec_url = "https://raw.githubusercontent.com/chemicaldawn/cs61b-cli/refs/heads/main/resources/coursespec.json"

def parse_args():
    parser : ArgumentParser = ArgumentParser(
        prog = "gitbug",
        description = "",
    )
    parser.add_argument("<repo-id>")
    parser.add_argument("<assignment-id>")
    parser.add_argument("output-path", nargs="?", default="./")
    parser.add_argument("-u","--update", action="store_true")
    args = parser.parse_args()
    return args

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

    student_repo_ssh = coursespec["student-repo-ssh"].replace("%",repo_id)
    course_repo_ssh = coursespec["course-repo-ssh"]

    os.chdir(clone_location)

    # set up student files
    run(["git","init"])
    sparse_checkout_location = ".git/info/sparse_checkout"

    run(["git","remote","add","student",student_repo_ssh])

    run(["git","sparse-checkout","init"])
    run(["git","sparse-checkout","set",f"{assignment_id}/"])

    run(["git","pull","student","main"]) 

    move(f"{assignment_id}/tests/",f"{assignment_id}/tests_student/")

    # set up grader files
    containing_folder = findall(r"([a-z]+)[0-9]", assignment_id)[0]
    tests_location = f"{containing_folder}/{assignment_id}/grader/submit/"

    run(["git","clone","--no-checkout",course_repo_ssh,".materials"])
    os.chdir(".materials")

    run(["git","sparse-checkout","init"])
    run(["git","sparse-checkout","set",f"{tests_location}/"])

    run(["git","checkout","main"])
    os.chdir("..")

    move(os.path.join(".materials",tests_location), f"{assignment_id}/tests_grader")

    # cleanup
    print("Cleaning up...")
    for root, dirs, files in os.walk(".materials", topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWRITE)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(".materials")
    print("Success! Happy debugging :)")

def main():
    args = vars(parse_args())
    check_file_structure()
    if (args["update"]):
        update(False)
    coursespec = get_coursespec()
    clone_down(args["<repo-id>"], args["<assignment-id>"], args["output-path"], coursespec)

if __name__ == "__main__":
    main()
    