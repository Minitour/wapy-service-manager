import requests
import sys
import json
import wapy_agent
import time
import os
import re


def main():
    # data = sys.argv[1]
    #
    # response = requests.post("http://localhost:8001/camera/{}".format(data), data=json.dumps({"mode": data}))
    #
    # print(response.status_code)
    # print(response.text)
    # command = "python facial_landmarks.py"
    #
    # out, errors = wapy_agent.execute_command(command)
    #
    # time.sleep(10)

    os.chdir("c:/Users/wapyi/Documents/wapy_src/CameraService")

    command = "ps aux | grep python"

    out, error = wapy_agent.execute_command(command)

    pid = -1

    for o in str(out).split("\\n"):
        out1 = o.lstrip('b')
        out1 = out1.lstrip('"')

        check_python_command = out1.find("python")
        if check_python_command != -1:
            print("found command")
            command1 = out1.split()
            try:
                pid = int(command1[0].strip())
            except Exception as error:
                print(error)

        else:
            print("command not found")
        print(out1)
        print("\n")


    if pid != -1:
        kill_command = "kill {}".format(pid)
        out, error = wapy_agent.execute_command(kill_command)
        print(out)
        print(error)
    
    # print(out)
    # print("\n\n")
    # print(error)


if __name__ == "__main__":
    main()