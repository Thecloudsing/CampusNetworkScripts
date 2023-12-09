import subprocess

build_command = "pyinstaller ./Dream.spec"
install_command = "pip install pyinstaller"
try:
    subprocess.run(["powershell.exe", "-Command", build_command], shell=True, check=True)
except:
    print('not found pyinstaller.exe')
    try:
        subprocess.run(["powershell.exe", "-Command", install_command], shell=True, check=True)
        print("start download install pyinstaller...")
    except:
        print("install error...")
        exit(1)

