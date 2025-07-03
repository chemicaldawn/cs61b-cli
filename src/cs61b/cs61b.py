import os
import json
from subprocess import run, Popen, PIPE
from argparse import ArgumentParser

cs61b_remote_repo = "git@github.com:chemicaldawn/cs61b-cli.git"
cs61b_folder = os.path.expanduser("~/.cs61b")
cs61b_local_repo = os.path.expanduser("~/.cs61b/primary")
course_materials_local_repo = os.path.expanduser("~/.cs61b/materials")
libraries_local_repo = os.path.expanduser("~/.cs61b/libraries")
coursespec_path = os.path.expanduser("~/.cs61b/primary/resources/coursespec.json")

def parse_args():
    parser : ArgumentParser = ArgumentParser(
        prog = "cs61b",
        description = "",
    )

    parser.add_argument("-u","--soft-update", action="store_true")
    parser.add_argument("-U","--hard-update", action="store_true")
    args = parser.parse_args()
    return args

def soft_update():
    print("Performing soft update...")

    if not os.path.exists(cs61b_folder):
        print("Creating cache folder...")
        os.mkdir(cs61b_folder)

    os.chdir(cs61b_folder)

    if not os.path.exists(cs61b_local_repo):
        print("Cloning source...")
        run(["git","clone",cs61b_remote_repo,"primary"])
    else:
        os.chdir(cs61b_local_repo)
        run(["git","pull","origin","main"])
        os.chdir("..")

    coursespec_file = open(coursespec_path,"r")
    coursespec = json.loads(coursespec_file.read())

    if not os.path.exists(course_materials_local_repo):
        print("Cloning course materials...")
        os.chdir(cs61b_folder)
        run(["git","clone",coursespec["course-repo-ssh"],"materials"])
    else:
        os.chdir(course_materials_local_repo)
        run(["git","pull","origin","main"])
        os.chdir("..")

    if not os.path.exists(libraries_local_repo):
        print("Cloning course materials...")
        os.chdir(cs61b_folder)
        run(["git","clone",coursespec["library-repo-ssh"],"libraries"])
    else:
        os.chdir(libraries_local_repo)
        run(["git","pull","origin","main"])
        os.chdir("..")


    print("Soft update finished!")


def hard_update():
    print("Performing hard update. Soft-updating first.")
    soft_update()  

def main():
    args = vars(parse_args())

    if (args["soft_update"]):
        soft_update()
    if (args["hard_update"]):
        hard_update()

if __name__ == "__main__":
    main()