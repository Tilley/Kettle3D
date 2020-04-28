versionlist = {
    "dev" : [
        [1, (20, 4, 'a')]
    ],
    "stable" : [
        #none yet...
    ]
}

# Updates need to be posted above with syntax as such:
# Developement versions go under "dev" and releases under "stable."
# dev[0][0] is the version number; 1 is the first version, 2 the second etc.
# The tuple contained within the array for the version is this:
# (<year released>, <month released>, <build name>). Please only add a single-letter build name corresponding to the order in which
# that month's versions were made.
# Feel free to make a pull request - put your version in the list. DO NOT MARK IT AS STABLE UNTIL I HAVE TESTED IT.
# Put the programming for the version in Kettle3D/versions/d20-04a.py. Add a txtfile object for all the text files, along with .py etc.
# Initialise the textfile under the play function. Make sure to add all required txtfiles and binaryfiles as well.

from tkinter import *
from urllib.request import urlopen
from os.path import normpath
from os import getenv
from os import getcwd

import os
import time
import sys
import pickle
import pathlib

# I've declared directory outside of the `if` block so it can be accessed in the global scope
directory = ''

# In Python, os.name is 'nt' if you are running on Windows
if os.name == 'nt': # do windows-specific things
    directory = getenv("%USERPROFILE%") + "\\AppData\\Roaming\\Kettle3D\\"
else:
    directory = getenv('HOME') + '/Library/Application Support/Kettle3D/'

# This function will create the directory, and any of the parent directories, if it does not exist.
# I've added the "asset" part with os.path.join, but any other directories in these folders would
# need to be created before creating files in them.
pathlib.Path(os.path.join(directory, 'assets')).mkdir(parents=True, exist_ok=True)

class file_dummy():
    def open(self, a=None, b=None, c=None):
        pass
    def close(self):
        pass
    def read(self):
        pass
    def write(self):
        pass

try:
    filelistfile = open(directory + normpath("assets/files.dat"), 'rb')
    files = pickle.load(filelistfile)
    print("Successfully retrieved file array.")
    filelistfile.close()
except (FileNotFoundError, OSError):
    filelistfile = open(directory + normpath("assets/files.dat"), 'xb')
    files = {# This is the filearray. It stores all the information needed to find other files, whether binary or normal text.
        "binary" : [
            {# This is a file entry as provided by the downloadfile class. This entry belongs to the file array itself.
                "path" : "assets/files.dat",
                "version" : 1
            }
        ],
        "txt" : [
        ]
    }
    pickle.dump(files, filelistfile)
    print("Successfully created a new filearray.")
    filelistfile.close()

class txtfile():
    def __init__(self, path, version, newcontent=None): # file for download
        self.path = path
        self.version = version
        self.winpath = normpath(self.path)
        self.newcontent = newcontent
        print("Looking for file %s..." % path)
        try:
            self.newcontent = open(directory + self.winpath, 'w')
            self.oldcontent = open(directory + self.winpath, 'r')
            print("File %s found successfully." % path)
            try:

                self.onlinecontent = urlopen("https://raw.githubusercontent.com/Kettle3D/Kettle3D/master/" + path).read().decode('utf-8')
                if self.oldcontent != self.onlinecontent:
                    self.newcontent.write(self.onlinecontent)
                    print("Successfully updated file.")
                else:
                    print("File matches.")
            except Exception as e:
                print("Couldn't update file. Maybe try checking your internet connection?")
                print(e)
        except (FileNotFoundError, OSError):
            self.newcontent = open(directory + self.winpath, 'x')
            print("File %s created successfully." % path)
            try:
                self.onlinecontent = urlopen("https://raw.githubusercontent.com/Kettle3D/Kettle3D/master/" + path).read().decode('utf-8')
                print("Successfully downloaded file.")
                fae = {
                    "path" : self.path,
                    "winpath" : self.winpath,
                    "version" : self.version
                }
                files['txt'].append(fae)
            except Exception as e:
                print("Couldn't download file. Maybe try checking your internet connection?")
                print(e)
        finally:
            self.newcontent.close()

class binaryfile():
    def __init__(self, path, version): # file for download
        self.path = path
        self.version = version
        self.winpath = normpath(self.path)
        print("Looking for file %s..." % path)
        try:
            self.newcontent = open(directory + self.winpath, 'wb')
            self.oldcontent = open(directory + self.winpath, 'rb')
            print("File %s found successfully." % path)
            try:
                self.onlinecontent = urlopen("https://raw.githubusercontent.com/Kettle3D/Kettle3D/master/" + path, 'rb').read().decode('utf-8')
                if self.oldcontent != self.onlinecontent:
                    self.newcontent.write(self.onlinecontent)
                    print("Successfully updated file.")
                else:
                    print("File matches.")
            except:
                print("Couldn't update file. Maybe try checking your internet connection?")
        except (FileNotFoundError, OSError):
            self.content = open(directory + self.winpath, 'xb')
            print("File %s created successfully." % path)
            try:
                self.onlinecontent = urlopen("https://raw.githubusercontent.com/Kettle3D/Kettle3D/master/" + path, 'rb').read().decode('utf-8')
                print("Successfully downloaded file.")
                fae = {
                    "path" : self.path,
                    "winpath" : self.winpath,
                    "version" : self.version
                }
                files['binary'].append(fae)
            except Exception as e:
                print("Couldn't download file. Maybe try checking your internet connection?")
                print(e)
        finally:
            self.content.close()

isdiropen = False
isplayopen = False
dir_tk = None
play_tk = None
tk = Tk()
tk.title("Kettle3D Launcher")
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

print("The launcher window opened successfully.")

print("Have 1 files to update or download.")

thomas = file_dummy()

assets_index = txtfile("assets/assets-index.py", 1, thomas)

print("Finished checking files.")

def play():
    isplayopen = True
    play_tk = Tk()
    play_tk.title("Versions - Kettle3D Launcher")
    play_tk.wm_attributes("-topmost", 1)
    play_canvas = Canvas(play_tk, width=250, height=250)
    play_canvas.pack()
    play_tk.update()
    tk.update()


def closedirwin():
    if isdiropen:
        dir_tk.destroy()
        dir_tk = None
        isdiropen = False

def launch():
    play_tk.destroy()
    isplayopen = False

def dir():
    # Change directory

    isdiropen = True

    dir_tk = Tk()
    dir_tk.title("Change Directory - Kettle3D Launcher")
    dir_tk.wm_attributes("-topmost", 1)
    dir_canvas = Canvas(dir_tk, width=500, height=20)
    dir_canvas.pack()
    dir_tk.update()
    tk.update()
    dirtxt = dir_canvas.create_text(250, 11, text="The directory is set to %s." % directory, font=('Helvetica', 15))

choosedir = Button(tk, text="Change Directory", command=dir)
playbtn = Button(tk, text="PLAY", command=play)
choosedir.pack()
playbtn.pack()
closebtn = Button(tk, text="Cancel", command=closedirwin)

while True:
    tk.update_idletasks()
    tk.update()
    if isdiropen:
        dir_canvas.itemconfig(dirtxt, x=dir_tk.winfo_width(), text="The directory is set to %s." % directory)
        dir_tk.update_idletasks()
        dir_tk.update()
    if isplayopen:
        play_tk.update_idletasks()
        play_tk.update()
    time.sleep(0.01)
