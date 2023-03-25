# Installs text-generation-webui from the repo in the tg folder.
# It creates the python virtual environment and installs requirements
# It also installs ROCm pytorch over the specified version

import os
import subprocess
import shutil

class TGInstaller:
    def __init__(self):
        self.WD = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'rocm-buntu'))
        self.TGPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tg'))
        self.TGEXEC = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tg', 'text-generation-webui'))
        self.TGENV = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tg', 'venv', 'bin'))
    
    def install(self):
        #create virtual environment
        if os.path.exists(self.TGENV):
            shutil.rmtree(self.TGENV)
        os.chdir(self.TGPATH)
        subprocess.run(["python3", "-m", "venv", "venv"])
        #install requirements
        os.chdir(self.TGEXEC)
        sproc = subprocess.Popen([self.TGENV+'/pip', "install", "-r", "requirements.txt"])
        sproc.wait()
        #install pytorch ROCm
        sproc = subprocess.Popen([self.TGENV+'/pip', "install", "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/rocm5.2"])
        sproc.wait()

if __name__ == "__main__":
    tginstaller = TGInstaller()
    tginstaller.install()