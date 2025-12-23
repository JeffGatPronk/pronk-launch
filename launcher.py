import sys
import subprocess
from urllib.parse import urlparse, parse_qs
import os

def main():
    if len(sys.argv) < 2:
        print("No Work Order provided")
        return

    url = sys.argv[1]
    qs = parse_qs(urlparse(url).query)
    workorder = qs.get("wo", [""])[0]

    if not workorder:
        print("Missing Work Order ID")
        return

    # Launch GUI in a separate detached process
    gui_exe = os.path.join(os.path.dirname(__file__), "picker_gui.exe")
    subprocess.Popen([gui_exe, workorder], creationflags=subprocess.DETACHED_PROCESS)

if __name__ == "__main__":
    main()
