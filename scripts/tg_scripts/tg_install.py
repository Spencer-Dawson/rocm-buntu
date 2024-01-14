# Installs text-generation-webui from the repo in the tg folder.
# It creates the python virtual environment and installs requirements
# It also installs ROCm pytorch over the specified version

import os
import subprocess
import shutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TGInstaller:
    def __init__(self, TGENV, TGEXEC, TGPATH):
        #Make sure TGENV is a full path string
        if not os.path.isabs(TGENV):
            raise ValueError("TGENV must be a full path string")
        #Make sure TGEXEC is a full path string
        if not os.path.isabs(TGEXEC):
            raise ValueError("TGEXEC must be a full path string")
        #Make sure TGPATH is a full path string
        if not os.path.isabs(TGPATH):
            raise ValueError("TGPATH must be a full path string")

        self.TGENV = TGENV
        self.TGEXEC = TGEXEC
        self.TGPATH = TGPATH

        logger.debug("TGPATH: " + self.TGPATH)
        logger.debug("TGEXEC: " + self.TGEXEC)
        logger.debug("TGENV: " + self.TGENV)

    def install(self):
        #create virtual environment
        if os.path.exists(self.TGENV):
            shutil.rmtree(self.TGENV)
        os.chdir(self.TGPATH)
        subprocess.run(["python3", "-m", "venv", "venv"])
        os.chdir(self.TGEXEC)
        #install pytorch ROCm
        sproc = subprocess.Popen([self.TGENV+'/pip', "install", "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/rocm5.6"])
        sproc.wait()
        #install requirements
        sproc = subprocess.Popen([self.TGENV+'/pip', "install", "-r", "requirements_amd.txt"])
        sproc.wait()

if __name__ == "__main__":
    tginstaller = TGInstaller()
    tginstaller.install()
