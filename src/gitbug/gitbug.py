import os
import stat
import json
import requests
import hashlib
from subprocess import run
from shutil import copy, copytree, move, rmtree
from re import findall
from argparse import ArgumentParser

cs61b_folder = os.path.expanduser("~/.cs61b")
materials_folder = os.path.expanduser("~/.cs61b/materials")
libraries_folder = os.path.expanduser("~/.cs61b/libraries")
coursespec_path = os.path.expanduser("~/.cs61b/primary/resources/coursespec.json")

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
    if not os.path.exists(coursespec_path):
        update(True)

def get_coursespec():
    coursespec_file = open(coursespec_path,"r")
    coursespec = coursespec_file.read()
    coursespec_file.close()
    return json.loads(coursespec)

def update(critical=False):
    
    print("Updating coursespec. Running cs61b -u")
    run(["cs61b","-u"])

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

    copytree(os.path.join(materials_folder,tests_location), f"{assignment_id}/tests")

    student_tests_stub = f"{assignment_id}/tests_student"
    for file in os.listdir(os.path.join(f"{assignment_id}/tests_student")):
        filename = file.split(".")[0]
        print(filename)
        old_location = os.path.join(student_tests_stub, file)
        new_location = os.path.join(f"{assignment_id}/tests", f"Student{file}")

        content = ""
        with open(old_location, "r+") as f:
            content = f.read()
            content = content.replace(filename,f"Student{filename}")
            f.close()

        if (os.path.exists(new_location)):
            os.remove(new_location)

        with open(new_location, "w") as f:
            f.write(content)
            f.close()

    print("Cleaning up...")
    rmtree(student_tests_stub)
    #autoimport_libraries(assignment_id)
    print("Success! Happy debugging :)")

def autoimport_libraries(project_folder : str):
    os.mkdir(os.path.join(project_folder,".idea"))
    idea_libs_folder = os.path.join(project_folder,".idea","libraries")
    os.mkdir(idea_libs_folder)
    library_file_content = f"""<component name="libraryTable">
    <library name="libraries">
        <CLASSES>
            <root url="file://{libraries_folder}"/>
        </CLASSES>
        <JAVADOC/>
        <SOURCES>
            <root url="file://{libraries_folder}"/>
        </SOURCES>
        <jarDirectory url="file://{libraries_folder}" recursive="false"/>
        <jarDirectory url="file://{libraries_folder}" recursive="false" type="SOURCES"/>
    </library>
</component>"""
    with open(os.path.join(idea_libs_folder,"libraries.xml"), "w") as file:
        file.write(library_file_content)
        file.close()

def main():
    args = vars(parse_args())
    check_file_structure()
    if (args["update"]):
        update(False)
    coursespec = get_coursespec()
    clone_down(args["<repo-id>"], args["<assignment-id>"], args["output-path"], coursespec)

if __name__ == "__main__":
    main()