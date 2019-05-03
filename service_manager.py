from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

debug = os.environ['DEBUG_SERVICE_MANAGER']

methods = ['POST']
if str(debug).lower() == "true":
    print("DEBUG MODE...")
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


@app.route('/camera/<mode>', methods=methods)
def change_camera_mode(mode):
    if (not debug and request.method == "GET") or (debug):
        print("debug mode, did not do anything" if debug else "Method not allowed")
        return

    mode_str = switcher_helper(mode)
    print("will {} the camera service".format(mode_str))
    command = "nssm {} camera-service".format(mode_str)
    change_mod(command)


@app.route('/calibration', methods=methods)
def change_calibration_mode():
    mode = request.form.get("mode")
    mode_str = switcher_helper(mode)
    print("will {} the calibration service".format(mode_str))
    if debug:
        print("debug mode, did not do anything")
        return
    command = "nssm {} calibration-service".format(mode_str)
    change_mod(command)


@app.route('/connectivity', methods=methods)
def change_connectivity_mode():
    mode = request.form.get("mode")
    mode_str = switcher_helper(mode)
    print("will {} the connectivity service".format(mode_str))
    if debug:
        print("debug mode, did not do anything")
        return
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