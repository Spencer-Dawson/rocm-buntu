# CLI tool for oogabooga's text-generation-webui for people running on ubuntu 22.04
# available commands are install, configure, start, startd, stop, stopd, update, and remove
# todo add support for update, and configure

# import modules
import argparse
import os
import sys
import subprocess
import shutil
import yaml
import logging
from baseclass import ToolCliBaseClass

from scripts import tg_pull
from scripts import tg_install
from scripts import tg_configure
# from scripts import tg_update
from scripts import tg_remove

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

class Tg(ToolCliBaseClass):
    def __init__(self):
        logger.debug("Running %s", sys._getframe())
        #call super class constructor with the name of the tool
        super().__init__("tg")
        self.EXECBASE = self.TOOLBASE + "/text-generation-webui"
        self.VENV = self.TOOLBASE + "/venv/bin"

    def _pull(self):
        logger.debug("Running %s", sys._getframe())
        puller = tg_pull.TGPuller()
        puller.pull()
        super()._pull()

    def _preinstall(self):
        logger.debug("Running %s", sys._getframe())
        super()._preinstall()

    def _install(self):
        logger.debug("Running %s", sys._getframe())
        installer = tg_install.TGInstaller()
        installer.install()
        super()._install()

    def _postinstall(self):
        logger.debug("Running %s", sys._getframe())
        super()._postinstall()

    def _configure(self):
        logger.debug("Running %s", sys._getframe())
        super()._configure()
        configurator = tg_configure.TGConfigurator()
        configurator.configure()

    def _update(self):
        super()._update()

    def _start(self):
        logger.debug("Running %s", sys._getframe())
        super()._start()
        #starts the daemon and passes in all remaining arguments
        #exec server.py from the EXECBASE folder using the python3 binary from the VENV folder and pass it all remaining arguments
        os.chdir(self.EXECBASE)
        spoc = subprocess.Popen([self.VENV + "/python3", self.EXECBASE + "/server.py"] + sys.argv[2:])        
        spoc.wait()

    def _startd(self):
        logger.debug("Running %s", sys._getframe())
        super()._startd()
        #starts the daemon and passes in all remaining arguments
        #exec server.py from the EXECBASE folder using the python3 binary from the VENV folder and pass it all remaining arguments
        os.chdir(self.EXECBASE)
        spoc = subprocess.Popen([self.VENV + "/python3", self.EXECBASE + "/server.py"] + sys.argv[2:])

    def _stop(self):
        logger.debug("Running %s", sys._getframe())
        super()._stop()
        #kills the daemon that was started by _startd
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
        remover = tg_remove.TGRemover()
        remover.remove()

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
    
    def startd(self):
        logger.debug("Running %s", sys._getframe())
        self._startd()

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
    commandgroup = parser.add_mutually_exclusive_group(required=True)
    commandgroup.add_argument('--install', action='store_true', help='install tg')
    #commandgroup.add_argument('--configure', action='store_true', help='configure tg')
    commandgroup.add_argument('--start', action='store_true', help='start tg')
    commandgroup.add_argument('--startd', action='store_true', help='start tg as a background process')
    commandgroup.add_argument('--stopd', action='store_true', help='stop tg background process')
    #commandgroup.add_argument('--update', action='store_true', help='update tg')
    commandgroup.add_argument('--remove', action='store_true', help='remove tg')
    args = parser.parse_args()

    # run command
    tg = Tg()
    if args.install:
        tg.install()
    #elif args.configure:
    #    tg.configure()
    elif args.start:
        tg.start()
    elif args.startd:
        tg.startd()
    elif args.stopd:
        tg.stop()
    #elif args.update:
    #    tg.update()
    elif args.remove:
        tg.remove()
