# Installs stable-diffusion-webui from the repo in the sd folder.
# It creates the python virtual environment and installs requirements
# see https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Install-and-Run-on-AMD-GPUs for reference

# sigh. my options are use the goofy webui script or reverse engineer and wrap launch py
# or install with webui and wrap launch.py when running
import os
import signal
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SDInstaller:
    def __init__(self, SDENV, SDEXECPATH, SDBASE):
        #Make sure SDENV is a full path string
        if not os.path.isabs(SDENV):
            raise ValueError("SDENV must be a full path string")
        #Make sure SDEXECPATH is a full path string
        if not os.path.isabs(SDEXECPATH):
            raise ValueError("SDEXECPATH must be a full path string")
        #Make sure SDBASE is a full path string
        if not os.path.isabs(SDBASE):
            raise ValueError("SDBASE must be a full path string")

        self.SDENV = SDENV
        self.SDEXECPATH = SDEXECPATH
        self.SDBASE = SDBASE
        self.EXECCMD = "TORCH_COMMAND='pip install torch torchvision --index-url https://download.pytorch.org/whl/rocm5.2' "
        self.EXECCMD += self.SDENV+"/python "
        self.EXECCMD += self.SDEXECPATH+"/launch.py --precision full --no-half"


    def install(self):
        #Stable Diffusion has it's own installer script, so we work with it as much as possible
        os.chdir(self.SDEXECPATH)
        #create virtual environment
        os.chdir(self.SDEXECPATH)
        if not os.path.exists(self.SDENV):
            subprocess.run(["python3.10", "-m", "venv", "venv"])

        #will need to replace pytorch command in webui-user.sh
        pytorchcmd = "TORCH_COMMAND='pip install torch torchvision "
        pytorchcmd += "--index-url https://download.pytorch.org/whl/rocm5.2' "
        #will need to replace COMMANDLINE_ARGS with the correct args
        commandlineargs = "COMMANDLINE_ARGS='--precision full --no-half'"

        with open("webui-user.sh", "r") as f:
            lines = f.readlines()
        with open("webui-user.sh", "w") as f:
            for line in lines:
                if line.startswith("#export TORCH_COMMAND"):
                    f.write("export " + pytorchcmd)
                elif line.startswith("#export COMMANDLINE_ARGS"):
                    f.write("export " + commandlineargs)
                else:
                    f.write(line)

        #run the EXECCMD
        os.chdir(self.SDEXECPATH)
        sproc = subprocess.Popen(". "+self.SDENV +"/activate && ./webui.sh", stdout=subprocess.PIPE, shell=True)
        #wait for the process to output line starting with "Running on local url" then stop it
        while True:
            for line in iter(sproc.stdout.readline, b''):
                if line != '':
                    logger.info(line)
                    if line.startswith(b"Running on local URL"):
                        logger.info("Stable Diffusion installed. Stopping webui")
                        #kill the stable-diffusion-webui process
                        pid = subprocess.check_output(["ps aux | grep stable-diffusion-webui | grep -v grep | awk '{print $2}'"], shell=True).strip()
                        if pid:
                            subprocess.call(["kill", "-9", pid])
                        break
                else:
                    break

    # Install using only installer script
    # doesn't seem to work :(
    # def install(self):
    #     #Stable Diffusion has it's own installer script, so we work with it as much as possible
    #     os.chdir(self.SDEXECPATH)
    #     sproc = subprocess.Popen("./webui.sh", stdout=subprocess.PIPE, shell=True)
    #     #wait for the process to output line starting with "Runing on local url" then stop it
    #     while True:
    #         for line in iter(sproc.stdout.readline, b''):
    #             if line != '':
    #                 if line.startswith(b"Running on local URL"):
    #                     logger.info("Stable Diffusion installed. Stopping webui")
    #                     sproc.kill()
    #                     break
    #                 else:
    #                     logger.info(line)
    #             else:
    #                 break

    # # Install without webui
    # # doesn't seem to work :(
    # def install(self):
    #     #create virtual environment
    #     os.chdir(self.SDEXECPATH)
    #     if not os.path.exists(self.SDENV):
    #         subprocess.run(["python3.10", "-m", "venv", "venv"])

    #     #install pytorch ROCm
    #     os.chdir(self.SDEXECPATH)
    #     pytorchcmd = self.SDENV + "/pip install torch torchvision "
    #     pytorchcmd += "--index-url https://download.pytorch.org/whl/rocm5.2' "
    #     sproc = subprocess.run(pytorchcmd, shell=True)
    #     sproc.wait()

    #     #install requirements
    #     os.chdir(self.SDEXECPATH)
    #     sproc = subprocess.Popen([self.SDENV+'/pip', "install", "-r", "requirements.txt"], shell=True)
    #     sproc.wait()

if __name__ == "__main__":
    sdinstaller = SDInstaller()
    sdinstaller.install()
