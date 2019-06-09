import requests
import sys
import json
import wapy_agent
import time


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

    command = "ps aux | grep python"

    out, error = wapy_agent.execute_command(command)

    print(out)
    print("\n\n")
    print(error)


if __name__ == "__main__":
    main()