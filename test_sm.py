import requests
import sys
import json

def main():
    data = sys.argv[1]

    response = requests.post("http://localhost:8001/camera/{}".format(data), data=json.dumps({"mode": data}))

    print(response.status_code)
    print(response.text)


if __name__ == "__main__":
    main()