import sys
import subprocess
import time
def install():
    print("Installing Requirements Package...")
    time.sleep(1)
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    print("Successfully Installed Requirements Package! You're Good To Go")
    time.sleep(2)
