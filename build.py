import os
import shutil
import subprocess

build = './build'
dist = './dist'
if os.path.isfile(build):
    os.remove(build)
if os.path.isdir(build):
    shutil.rmtree(build)
if os.path.isfile(dist):
    os.remove(dist)
if os.path.isdir(dist):
    shutil.rmtree(dist)
build_command = "pyinstaller ./Dream.spec"
install_command = "pip install pyinstaller"
try:
    subprocess.run(["powershell.exe", "-Command", build_command], shell=True, check=True)
except:
    print('not found pyinstaller.exe')

