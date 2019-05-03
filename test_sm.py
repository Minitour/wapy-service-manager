import requests
import sys
import json

def main():
    data = sys.argv[1]

    response = requests.post("localhost:8001/camera/{}".format(data), data=json.dumps({"mode": 1}))

    print(response.status_code)
    print(response.text)


if __name__ == "__main__":
    main()