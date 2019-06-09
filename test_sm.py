import wapy_agent
import os
import sys
import service_manager

def main():

    mode = int(sys.argv[1])

    if mode == 0:
        service_manager.kill_camera_service()
    if mode == 1:
        service_manager.start_camera_service()
    return 0


if __name__ == "__main__":
    main()