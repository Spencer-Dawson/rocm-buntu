# # CLI tool for automatic111's stable-diffusion-webui for people running on ubuntu 22.04
# available commands are install, configure, start, startd, stop, stopd, update, and remove

# import modules
import argparse
import os
import sys
import subprocess
import shutil
import logging
from baseclass import ToolCliBaseClass

from scripts.utils import git_pull
from scripts.sd_scripts import sd_install
from scripts.sd_scripts import sd_configure
# from scripts import sd_update

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

class Sd(ToolCliBaseClass):
    def __init__(self):
        logger.debug("Running %s", sys._getframe())
        #call super class constructor with the name of the tool
        super().__init__("sd")
        self.EXECBASE = self.TOOLBASE + "/stable-diffusion-webui/"
        self.VENV = self.EXECBASE + "/venv/bin/"
        self.REPO = "https://github.com/AUTOMATIC1111/stable-diffusion-webui"

    def _pull(self):
        logger.debug("Running %s", sys._getframe())
        logger.debug("Pulling from %s", self.REPO)
        logger.debug("Pulling to %s", self.TOOLBASE)
        puller = git_pull.GitPuller(self.REPO, self.TOOLBASE)
        puller.pull()
        super()._pull()

    def _preinstall(self):
        logger.debug("Running %s", sys._getframe())
        super()._preinstall()

    def _install(self):
        logger.debug("Running %s", sys._getframe())
        logger.debug("Installing %s in %s", self.NAME, self.EXECBASE)
        installer = sd_install.SDInstaller(self.VENV, self.EXECBASE, self.TOOLBASE)
        installer.install()
        super()._install()

    def _postinstall(self):
        logger.debug("Running %s", sys._getframe())
        super()._postinstall()

    def _configure(self):
        logger.debug("Running %s", sys._getframe())
        configurer = sd_configure.SDConfigurator(self.CONFIGFOLDER + self.CONFIGFILE, \
                                                 self.CONFIGFOLDER + self.DEFAULTCONFIGFILE, self.EXECBASE, self.VENV)
        configurer.configure()
        super()._configure()

    def _remove(self):
        logger.debug("Running %s", sys._getframe())
        super()._remove()
        print("Are you sure you want to remove " + self.NAME + "?")
        print("This will remove all files and directories associated with " + self.NAME + ".")
        print("This cannot be undone.")
        print("Type 'yes' to continue.")
        confirmation = input()
        if confirmation != "yes":
            print("Aborting.")
            sys.exit()
        else:
            #delete the toolbase folder
            shutil.rmtree(self.TOOLBASE)

    def _start(self):
        logger.debug("Running %s", sys._getframe())
        super()._start()
        os.chdir(self.EXECBASE)
        spoc = subprocess.Popen([self.VENV + "/python3", self.EXECBASE + "/launch.py"] + sys.argv[2:])
        spoc.wait()

    def _startd(self):
        logger.debug("Running %s", sys._getframe())
        os.chdir(self.EXECBASE)
        spoc = subprocess.Popen([self.VENV + "/python3", self.EXECBASE + "/launch.py"] + sys.argv[2:])


    def _stop(self):
        logger.debug("Running %s", sys._getframe())
        super()._stop()
        #kill the stable-diffusion-webui process
        pid = subprocess.check_output(["ps aux | grep stable-diffusion-webui | grep -v grep | awk '{print $2}'"], shell=True).strip()
        if pid:
            subprocess.call(["kill", "-9", pid])

    def _update(self):
        logger.debug("Running %s", sys._getframe())
        super()._update()

    def install(self):
        logger.debug("Running %s", sys._getframe())
        self._pull()
        self._preinstall()
        self._install()
        self._postinstall()
        self._configure()
    def configure(self):
        logger.debug("Running %s", sys._getframe())
        self._configure()

    def start(self):
        logger.debug("Running %s", sys._getframe())
        self._start()

    def stop(self):
        logger.debug("Running %s", sys._getframe())
        self._stop()

    def update(self):
        logger.debug("Running %s", sys._getframe())
        self._update()

    def startd(self):
        logger.debug("Running %s", sys._getframe())
        self._startd()

    def remove(self):
        logger.debug("Running %s", sys._getframe())
        self._remove()

if __name__ == "__main__":
    logger.debug("Running %s", sys._getframe())

    # parse arguments
    parser = argparse.ArgumentParser()
    commandgroup = parser.add_mutually_exclusive_group(required=True)
    commandgroup.add_argument("-i", "--install", action="store_true", help="install the tool")
    commandgroup.add_argument("-c", "--configure", action="store_true", help="configure the tool")
    commandgroup.add_argument("-s", "--start", action="store_true", help="start the tool")
    commandgroup.add_argument("-d", "--startd", action="store_true", help="start the tool in daemon mode")
    commandgroup.add_argument("-p", "--stopd", action="store_true", help="stop the tool in daemon mode")
    #commandgroup.add_argument("-u", "--update", action="store_true", help="update the tool")
    commandgroup.add_argument("-r", "--remove", action="store_true", help="remove the tool")
    args = parser.parse_args()

    # run the tool
    sd = Sd()
    if args.install:
        sd.install()
    elif args.configure:
        sd.configure()
    elif args.start:
        sd.start()
    elif args.startd:
        sd.startd()
    elif args.stopd:
        sd.stop()
    # elif args.update:
    #     sd.update()
    elif args.remove:
        sd.remove()
