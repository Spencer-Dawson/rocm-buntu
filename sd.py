#!/usr/bin/python3
"""
A CLI tool for installing, configuring, and running stable-diffusion-webui
available commands are install, configure, start, stop, run, configure, update, install, and remove
"""

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

logging.basicConfig(level=logging.info)
logger = logging.getLogger(__name__)

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

    def _run(self, extra_args):
        logger.debug("Running %s", sys._getframe())
        super()._start()
        os.chdir(self.EXECBASE)
        spoc = subprocess.Popen([self.VENV + "/python3", self.EXECBASE + "/launch.py"] + extra_args)
        spoc.wait()

    def _start(self, extra_args):
        logger.debug("Running %s", sys._getframe())
        os.chdir(self.EXECBASE)
        spoc = subprocess.Popen([self.VENV + "/python3", self.EXECBASE + "/launch.py"] + extra_args)


    def _stop(self):
        logger.debug("Running %s", sys._getframe())
        super()._stop()
        #kill the stable-diffusion-webui process
        pid = subprocess.check_output(["ps aux | grep launch.py | grep -v grep | awk '{print $2}'"], shell=True).strip()
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

    def start(self, extra_args):
        logger.debug("Running %s", sys._getframe())
        self._start(extra_args=extra_args)

    def stop(self):
        logger.debug("Running %s", sys._getframe())
        self._stop()

    def run(self, extra_args):
        logger.debug("Running %s", sys._getframe())
        self._run(extra_args=extra_args)

    def update(self):
        logger.debug("Running %s", sys._getframe())
        self._update()

    def remove(self):
        logger.debug("Running %s", sys._getframe())
        self._remove()

if __name__ == "__main__":
    logger.debug("Running %s", sys._getframe())

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['start', 'stop', \
                                            'run', \
                                            'install', 'remove', \
                                            'update', 'configure'])
    parser.add_argument('extra_args', nargs=argparse.REMAINDER, default=[])

    args = parser.parse_args()

    sd = Sd()
    if args.command == "start":
        sd.start(extra_args=args.extra_args)
    elif args.command == "stop":
        sd.stop()
    elif args.command == "run":
        sd.run(extra_args=args.extra_args)
    elif args.command == "install":
        sd.install()
    elif args.command == "remove":
        sd.remove()
    elif args.command == "update":
        sd.update()
    elif args.command == "configure":
        sd.configure()
