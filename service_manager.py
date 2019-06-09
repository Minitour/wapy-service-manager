from flask import Flask, request
import subprocess
import os
import wapy_agent

app = Flask(__name__)

#debug = os.environ['DEBUG_SERVICE_MANAGER']
debug = True

camera_service_path = "c:/Users/wapyi/Documents/wapy_src/CameraService"

methods = ['POST']
if str(debug).lower() == "true":
    methods.append("GET")


##############
# modes:
# 0 - stop
# 1 - start
# 2 - restart
##############
def switcher_helper(mode):
    try:
        return {
            "0": "stop",
            "1": "start",
            "2": "restart"
        }[str(mode)]
    except Exception as error:
        print("error: {}".format(error))
        return ""


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


def kill_camera_service():
    # change dir to camera service
    os.chdir(camera_service_path)

    # command to get all python execs
    command = "ps aux | grep python"

    # get the out put (will get the pid from it)
    out, error = execute_command(command)

    # init the pid for the camera_service
    pids = []

    # checking if the camera serivce is running
    for o in str(out).split("\\n"):
        out1 = o.lstrip('b')
        out1 = out1.lstrip('"')

        check_python_command = out1.find("python")
        if check_python_command != -1:
            command1 = out1.split()
            try:
                pid_temp = int(command1[0].strip())
                pids.append(pid_temp)
            except Exception as error:
                print(error)

    if pids:
        for pid in pids:
            kill_command = "kill {}".format(pid)
            out, error = execute_command(kill_command)
            if not error:
                print("camera service stopped")
    else:
        print("camera service is not running...")


def start_camera_service():
    os.chdir(camera_service_path)
    command = "python facial_landmarks.py"
    out, error = execute_command(command)
    print(out)


@app.route('/camera/<mode>', methods=methods)
def change_camera_mode(mode):
    if request.method == "GET":
        print("Method not allowed")
        if debug:
            print("debug mode...")
        return

    mode_str = switcher_helper(mode)
    print("will {} the camera service".format(mode_str))
    command = "nssm {} camera-service".format(mode_str)
    change_mod(command)
    # if mode == 0:
    #     print("will stop the camera service")
    #     kill_camera_service()
    #
    # if mode == 1:
    #     print("will start the camera service")
    #     start_camera_service()


@app.route('/calibration/<mode>', methods=methods)
def change_calibration_mode(mode):
    if request.method == "GET":
        print("Method not allowed")
        if debug:
            print("debug mode...")
        return

    mode_str = switcher_helper(mode)
    print("will {} the calibration service".format(mode_str))
    command = "nssm {} calibration-service".format(mode_str)
    change_mod(command)


@app.route('/connectivity/<mode>', methods=methods)
def change_connectivity_mode(mode):
    if request.method == "GET":
        print("Method not allowed")
        if debug:
            print("debug mode...")
        return

    mode_str = switcher_helper(mode)
    print("will {} the connectivity service".format(mode_str))
    command = "nssm {} connectivity-service".format(mode_str)
    change_mod(command)


def change_mod(command):

    MyOut = subprocess.Popen(str(command).split(" "),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
    stdout,stderr = MyOut.communicate()
    print(stdout)
    print(stderr)


if __name__ == "__main__":
    app.run(port=os.environ['SERVICE_MANAGER_SERVER_PORT'])