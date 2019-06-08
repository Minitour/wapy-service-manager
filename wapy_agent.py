import subprocess
import os, sys
import shutil
from .service_manager import change_camera_mode, change_calibration_mode

environment_variable_git_repo = "GIT_REPO_LOCATION"
repos_to_zip = ["wapy-camera-service", "wapy-calibration-service"]

REQUIREMENTS_PATH_ERROR = 1
REQUIREMENTS_PATH_CHANGE_ERROR = 2
INSTALL_REQUIREMENTS_ERROR = 3


def get_requirements_path_in_repo(repo):
    return {
        "wapy-camera-service": {
            "path": "CameraService",
            "command": "python -m pip install -r requirements.txt"
        },
        "wapy-calibration-service": {
            "path": ".",
            "command": "npm install"
        }
    }[repo]


def execute_command(command):

    try:
        MyOut = subprocess.Popen(command.split(),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)

        # getting errors and the output
        return MyOut.communicate()
    except Exception as error:
        print("ERROR: failed to execute command: {}".format(command))
        return "","ERROR"


def backup_repo_before_update(repo):
    os.chdir("..")
    try:
        print("\tINFO: backing up repo {} before fetching and install updates".format(repo))

        shutil.make_archive("./backups/backup_repo_{}".format(repo), 'zip', repo)
        print("\tINFO: {} repo backed up".format(repo))
    except Exception as error:
        print(error)
        return False

    check_cd = cd_into_repo(repo)
    if not check_cd:
        return True
    else:
        return False


def update_local_code_repo(repo):

    print("INFO: starting to update packages...")
    # get into the path to repo with the requirements for new code
    try:
        repo_object = get_requirements_path_in_repo(repo)
        path_to_repo_requirements = repo_object['path']
        check_cd = cd_into_repo(path_to_repo_requirements)
        if check_cd:
            return REQUIREMENTS_PATH_ERROR
    except Exception as error:
        print(error)
        return REQUIREMENTS_PATH_ERROR

    try:
        # install the new components we need for the new code
        command = repo_object['command']
        stdout_update, stderr_update = execute_command(command)
        if stderr_update:
            return INSTALL_REQUIREMENTS_ERROR
        if stdout_update:
            for out in str(stdout_update).split("\\n"):
                out = out.lstrip('b')
                out = out.lstrip('"')
                if out != "":
                    print(out)

        print("INFO: repo {} packages has been updated!".format(repo))
        if repo == "wapy-camera-service":
            os.chdir("..")
        return 0
    except Exception as error:
        print(error)
        return INSTALL_REQUIREMENTS_ERROR


def main():
    os.chdir("..")
    general_errors = 0
    print("INFO: checking for git changes in all repos...")
    for repo in repos_to_zip:

        print("-"*80)
        changed_path = False

        print("INFO: checking for changes in {} repo".format(repo))
        print("INFO: cd into repo...")
        check_cd_into_repo = cd_into_repo(repo)

        if check_cd_into_repo:
            print("ERROR: continue to the next repo...")
            continue

        cmd, errors = execute_command("git checkout master")

        # diff from git
        command = "git diff master origin/master".format(repo, repo)
        stdout, stderr = execute_command(command)

        if stdout and not stderr:
            print("INFO: there are changes, will pull now...")

            # # backing up the repo before updating the repo - in case of failure
            # if not backup_repo_before_update(repo):
            #     return False

            # getting the new files from repo
            command = "git pull"
            stdout_pull, stderr_pull = execute_command(command)

            # checking for errors while fetching
            if stderr_pull:
                print("ERROR: Got errors while fetching repo {} from git: \n{}\n".format(repo, stderr_pull))
                continue

            print("INFO: changes fetched from git, code has been updated...")

            # update the components for python code
            check = update_local_code_repo(repo)

            # checking the return code after updating repos
            if check:
                general_errors = general_errors + 1 if check == INSTALL_REQUIREMENTS_ERROR else general_errors
                changed_path = True if check != REQUIREMENTS_PATH_CHANGE_ERROR and check != REQUIREMENTS_PATH_ERROR else False

            else:
                changed_path = True
                print("INFO: Done updating!")

        elif not stderr:
            changed_path = True
            print("INFO: NO changes in repo!")

        if stderr:
            print("ERROR: got some errors while fetching repo from git: \n{}".format(stderr))

        if changed_path:
            # return to the main folder with all repos
            os.chdir("..")

    print("-"*80)
    if repos_to_zip and not general_errors:
        print("---- FINAL INFO: all repos has been updated! ----")
    elif general_errors == len(repos_to_zip):
        print("---- FINAL INFO: NONE of the repos has been updated ----")
    else:
        print("---- FINAL INFO: some repos has not been updated, check log above ----")

    if general_errors:
       roll_back()


def roll_back():
    print("ERROR: rolling back...")
    print("ERROR: stopping all services: {}".format(", ".join(repos_to_zip)))
    stop_services()

    for repo in repos_to_zip:
        print("SENSITIVE: rolling back repo {}".format(repo))
        # remove current repo - maybe corrupted
        check_removal = remove_repo(repo)

        if check_removal:
            print("SENSITIVE: removed current repo...")
        else:
            print("\n!----- SENSITIVE: something went wrong removing files! -----!\n")
            continue

    print("Removed all Repos -> waiting for the next run that the agent will pull from git")


def remove_repo(repo):
    print("\tSENSITIVE: removing repo...")
    command = "rmdir {} /s".format(repo)
    stdout, stderr = execute_command(command)
    if not stderr:
        return True
    else:
        return False


def stop_services():
    change_camera_mode(0)
    change_calibration_mode(0)


def cd_into_repo(repo):

    try:
        os.chdir(os.path.abspath(repo))
    except Exception as error:
        print(error)
        return REQUIREMENTS_PATH_CHANGE_ERROR

    return 0

if __name__ == "__main__":
    main()
