from urllib.request import urlopen
import sys

try:
#if True:
        launcherprogramming = urlopen("https://raw.githubusercontent.com/Kettle3D/Kettle3D/master/kettle3D-versions.py").read().decode('utf-8')
        print("Checking for updates")

        try:
        	launcher = open("C:\\Program Files\\Kettle3D\\kettle3DLauncher.py", 'w')
        	o = open("C:\\Program Files\\Kettle3D\\kettle3DLauncher.py", 'r')
        	old_launcher = o.read()
        	is_new = False
        except:
        	launcher = open("C:\\Program Files\\Kettle3D\\kettle3DLauncher.py", 'x')
        	is_new = True

        launcher.write(launcherprogramming)
        launcher.close()
        if is_new:
        	print("Successfully installed Kettle3D launcher")
        elif not old_launcher == launcherprogramming:
        	print("Updated Kettle3D Successfully")
        else:
        	print("Kettle3D is up to date")
except:
	print("Kettle3D couldn't check for updates. Try checking your internet connection.")

sys.path.append("C:\\Program Files\\Kettle3D")

import kettle3DLauncher
