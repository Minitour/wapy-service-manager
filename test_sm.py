import requests
import sys

def main():
    data = sys.argv[1]

    response = requests.post("localhost:8001/camera/{}".format(data))

    print(response.status_code)
    print(response.text)


if __name__ == "__main__":
    main()