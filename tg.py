#!/usr/bin/python3
"""
A CLI tool for installing, configuring, and running text-generation-webui
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
from scripts.tg_scripts import tg_install
from scripts.tg_scripts import tg_configure

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Tg(ToolCliBaseClass):
    def __init__(self):
        logger.debug("Running %s", sys._getframe())
        #call super class constructor with the name of the tool
        super().__init__("tg")
        self.EXECBASE = self.TOOLBASE + "text-generation-webui/"
        self.VENV = self.TOOLBASE + "venv/bin/"
        self.REPO = "https://github.com/oobabooga/text-generation-webui"

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
        installer = tg_install.TGInstaller(self.VENV, self.EXECBASE, self.TOOLBASE)
        installer.install()
        super()._install()

    def _postinstall(self):
        logger.debug("Running %s", sys._getframe())
        super()._postinstall()

    def _configure(self):
        logger.debug("Running %s", sys._getframe())
        super()._configure()
        configurator = tg_configure.TGConfigurator(self.CONFIGFOLDER + self.CONFIGFILE, \
                                                   self.CONFIGFOLDER +  self.DEFAULTCONFIGFILE, \
                                                    self.EXECBASE, self.VENV)
        configurator.configure()

    def _update(self):
        super()._update()

    def _run(self, extra_args):
        logger.debug("Running %s", sys._getframe())
        super()._run()
        #starts the server and passes in all remaining arguments
        #exec server.py from the EXECBASE folder using the python3 binary from the VENV folder and pass it all remaining arguments
        os.chdir(self.EXECBASE)
        spoc = subprocess.Popen([self.VENV + "/python3", self.EXECBASE + "/server.py"] + extra_args)
        spoc.wait()

    def _start(self, extra_args):
        logger.debug("Running %s", sys._getframe())
        #starts the daemon and passes in all remaining arguments
        #exec server.py from the EXECBASE folder using the python3 binary from the VENV folder and pass it all remaining arguments
        os.chdir(self.EXECBASE)
        spoc = subprocess.Popen([self.VENV + "/python3", self.EXECBASE + "/server.py"] + extra_args)

    def _stop(self):
        logger.debug("Running %s", sys._getframe())
        super()._stop()
        #kills the daemon that was started by _start
        #get the pid of the server.py python process
        pid = subprocess.check_output(["pgrep", "-f", self.EXECBASE + "/server.py"]).decode("utf-8")
        #kill the process
        subprocess.run(["kill", pid])

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

    def run(self, extra_args):
        logger.debug("Running %s", sys._getframe())
        self._run(extra_args=extra_args)

    def start(self, extra_args):
        logger.debug("Running %s", sys._getframe())
        self._start(extra_args=extra_args)

    def stop(self):
        logger.debug("Running %s", sys._getframe())
        self._stop()

    def update(self):
        logger.debug("Running %s", sys._getframe())
        self._update()

    def remove(self):
        logger.debug("Running %s", sys._getframe())
        self._remove()

if __name__ == '__main__':
    logger.debug("Running %s", sys._getframe())

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['start', 'stop', \
                                            'run', \
                                            'install', 'remove', \
                                            'update', 'configure'])
    parser.add_argument('extra_args', nargs=argparse.REMAINDER, default=[])

    args = parser.parse_args()

    # run command
    tg = Tg()
    if args.command == "start":
        tg.start(extra_args=args.extra_args)
    elif args.command == "stop":
        tg.stop()
    elif args.command == "run":
        tg.run(extra_args=args.extra_args)
    elif args.command == "install":
        tg.install()
    elif args.command == "remove":
        tg.remove()
    elif args.command == "update":
        tg.update()
    elif args.command == "configure":
        tg.configure()
