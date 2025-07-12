import os

def clone_or_update(local_repo_path : str, remote_repo_path: str, clone_root: str):
    if not os.path.exists(local_repo_path):
        print("Cloning course materials...")
        os.chdir(clone_root)
        run(["git","clone",remote_repo_path,"materials"])
    else:
        os.chdir(local_repo_path)
        run(["git","pull","origin","main"])
        os.chdir("..")