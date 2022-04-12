import sys
import subprocess
import pkg_resources
import os
import time
def install():
 if os.name == 'nt':
    required = {'discum', 'inputimeout', 'discord_webhook'}
 if os.name != 'nt':
    required = {'discum', 'simplejson', 'inputimeout', 'discord_webhook'}
 installed = {pkg.key for pkg in pkg_resources.working_set}
 missing = required - installed
 if not missing:
    print("Requirement Package Are Installed Already! You're Good To Go")
    time.sleep(2)
 if missing:
    print("Installing Requirements Package...")
    time.sleep(1)
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
    print("Successfully Installed Requirements Package! You're Good To Go")
    time.sleep(2) 
