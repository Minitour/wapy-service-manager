import requests
import sys
import json
import wapy_agent
import time
import os


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

    for o in str(out).split("\\n"):
        out1 = o.lstrip('b')
        out1 = out1.lstrip('"')
        if out1 != "":
            print(out1)
    print(out)
    print("\n\n")
    print(error)


if __name__ == "__main__":
    main()