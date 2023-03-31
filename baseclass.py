# Installs Necessary Packages for using ROCm based ml tools on Ubuntu 22.04
# Also includes abstract base class for tool wrappers
# Author: Spencer Dawson
# Note: Don't go deeper than 1 more level of abstraction than shown
#       here. If you need to go deeper, you're probably going to
#       introduce difficult to debug issues and confuse other devs.

import os
import sys
import subprocess
from abc import ABC, abstractmethod
import logging

#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class PackageManagerBaseClass(ABC):
    """
    Package Manager class wrapper
    This is an abstract base class that provides the structure for
    a package manager to implement to behave consistently with the
    rest of the package wrappers. It also provies some helper
    functions
    """

    @abstractmethod
    def __init__(self, name):
        logger.debug("Running %s", sys._getframe())

        # sets global constants and checks for OS compatability
        # some of these are not used in some derived classes
        # for example ROCm Instalation doesn't need a toolbase directory

        # name of the tool
        self.NAME = name
        # working directory
        self.WD = os.getcwd() + '/'
        # config folder
        self.CONFIGFOLDER = self.WD + 'config/'
        # script folder
        self.SCRIPTFOLDER = self.WD + 'scripts/'
        # config file
        self.CONFIGFILE = self.NAME + "-user.yml"
        # default config file
        self.DEFAULTCONFIGFILE = self.NAME + "-default.yml"
        # tool base directory
        self.TOOLBASE = self.WD + self.NAME +'/'

        try:
            # os name pulled from system
            self.OSNAME = os.uname().sysname
            assert self.OSNAME == 'Linux', "This utility only supports ubuntu 22.04"
            # os version pulled from system
            self.OSRELEASE = os.uname().release
            # os architecture pulled from system
            self.OSARCH = os.uname().machine
            logging.debug("OSARCH: %s", self.OSARCH)
            assert self.OSARCH == 'x86_64', "This utility only supports ubuntu 22.04"
            # os kernel version pulled from system
            self.OSVERSION = os.uname().version
            logging.debug("OSVERSION: %s", self.OSVERSION)
            #assert self.OSKERNEL contains ubuntu and 22.04
            assert 'ubuntu' in self.OSVERSION.lower(), "This utility only supports ubuntu 22.04"
            assert '22.04' in self.OSVERSION.lower(), "This utility only supports ubuntu 22.04"
        except AssertionError as e:
            logger.error("This utility only supports Ubuntu 22.04")
            sys.exit(1)

        #check if amd card is present
        self.AMDGPU = self._check_amd_gpu()
        assert self.AMDGPU == True, "This utility only supports AMD GPUs"
        #check if rocm is installed
        self.ROCM = self._check_rocm()
        assert self.ROCM == True, "ROCm is not installed. Please install ROCm before running this utility"

        #print global consts for debugging
        logger.debug("NAME: %s", self.NAME)
        logger.debug("WD: %s", self.WD)
        logger.debug("CONFIGFOLDER: %s", self.CONFIGFOLDER)
        logger.debug("SCRIPTFOLDER: %s", self.SCRIPTFOLDER)
        logger.debug("CONFIGFILE: %s", self.CONFIGFILE)
        logger.debug("DEFAULTCONFIGFILE: %s", self.DEFAULTCONFIGFILE)
        logger.debug("TOOLBASE: %s", self.TOOLBASE)
        logger.debug("OSNAME: %s", self.OSNAME)
        logger.debug("OSRELEASE: %s", self.OSRELEASE)
        logger.debug("OSARCH: %s", self.OSARCH)
        logger.debug("OSVERSION: %s", self.OSVERSION)
        logger.debug("AMDGPU: %s", self.AMDGPU)
        logger.debug("ROCM: %s", self.ROCM)


    def _check_amd_gpu(self):
        logger.debug("Running %s", sys._getframe())
        try:
            lspci = subprocess.check_output('lspci | grep -i vga', shell=True, universal_newlines=True)
            logging.debug("lspci: %s", lspci)
            if 'amd' in lspci.lower():
                return True
            else:
                return False
        except subprocess.CalledProcessError as e:
            logger.error("Error running lspci: %s", e)
            sys.exit(1)

    def _check_rocm(self):
        logger.debug("Running %s", sys._getframe())
        try:
            rocm = subprocess.check_output('which rocm-smi', shell=True, universal_newlines=True)
            logging.debug("rocm-smi: %s", rocm)
            if rocm:
                return True
            else:
                return False
        except subprocess.CalledProcessError as e:
            logger.error("Error running rocm-smi: %s", e)
            sys.exit(1)

    @abstractmethod
    def _pull(self):
        logger.debug("Running %s", sys._getframe())
        pass

    @abstractmethod
    def _preinstall(self):
        logger.debug("Running %s", sys._getframe())
        pass

    @abstractmethod
    def _install(self):
        logger.debug("Running %s", sys._getframe())
        pass

    @abstractmethod
    def _postinstall(self):
        logger.debug("Running %s", sys._getframe())
        pass

    @abstractmethod
    def _configure(self):
        logger.debug("Running %s", sys._getframe())
        pass

    @abstractmethod
    def _update(self):
        logger.debug("Running %s", sys._getframe())
        pass

    @abstractmethod
    def _remove(self):
        logger.debug("Running %s", sys._getframe())
        pass

    @abstractmethod
    def install(self):
        logger.debug("Running %s", sys._getframe())
        self._pull()
        self._preinstall()
        self._install()
        self._postinstall()
        self._configure()

    @abstractmethod
    def configure(self):
        logger.debug("Running %s", sys._getframe())
        self._configure()

    @abstractmethod
    def update(self):
        logger.debug("Running %s", sys._getframe())
        self._update()

    @abstractmethod
    def remove(self):
        logger.debug("Running %s", sys._getframe())
        self._remove()

class ToolCliBaseClass(PackageManagerBaseClass):
    """
    Tool class wrapper
    This is an abstract base class that provides the structure for
    a tool to implement to behave consistently with the
    rest of the tool wrappers. It also provies some helper functions
    """

    @abstractmethod
    def __init__(self, name):
        logger.debug("Running %s", sys._getframe())
        super().__init__(name)

    @abstractmethod
    def _pull(self):
        logger.debug("Running %s", sys._getframe())
        super()._pull()

    @abstractmethod
    def _preinstall(self):
        logger.debug("Running %s", sys._getframe())
        super()._preinstall()

    @abstractmethod
    def _install(self):
        logger.debug("Running %s", sys._getframe())
        super()._install()

    @abstractmethod
    def _postinstall(self):
        logger.debug("Running %s", sys._getframe())
        super()._postinstall()

    @abstractmethod
    def _configure(self):
        logger.debug("Running %s", sys._getframe())
        super()._configure()

    @abstractmethod
    def _update(self):
        logger.debug("Running %s", sys._getframe())
        super()._update()

    @abstractmethod
    def _start(self):
        logger.debug("Running %s", sys._getframe())
        pass

    @abstractmethod
    def _stop(self):
        logger.debug("Running %s", sys._getframe())
        pass

    @abstractmethod
    def _remove(self):
        logger.debug("Running %s", sys._getframe())
        super()._remove()

    @abstractmethod
    def install(self):
        logger.debug("Running %s", sys._getframe())
        self._pull()
        self._preinstall()
        self._install()
        self._postinstall()
        self._configure()

    @abstractmethod
    def configure(self):
        logger.debug("Running %s", sys._getframe())
        self._configure()

    @abstractmethod
    def start(self):
        logger.debug("Running %s", sys._getframe())
        super()._start()

    @abstractmethod
    def stop(self):
        logger.debug("Running %s", sys._getframe())
        self._stop()

    @abstractmethod
    def update(self):
        logger.debug("Running %s", sys._getframe())
        self._update()

    @abstractmethod
    def remove(self):
        logger.debug("Running %s", sys._getframe())
        self._remove()

class ToolCliWrapperTestClass(ToolCliBaseClass):
    """
    Tool class wrapper test class
    This is a unit test function for the ToolCliBaseClass
    """

    def __init__(self, name):
        logger.debug("Running %s", sys._getframe())
        super().__init__(name)

    def _pull(self):
        logger.debug("Running %s", sys._getframe())
        super()._pull()

    def _preinstall(self):
        logger.debug("Running %s", sys._getframe())
        super()._preinstall()

    def _install(self):
        logger.debug("Running %s", sys._getframe())
        super()._install()

    def _postinstall(self):
        logger.debug("Running %s", sys._getframe())
        super()._postinstall()

    def _configure(self):
        logger.debug("Running %s", sys._getframe())
        super()._configure()

    def _update(self):
        logger.debug("Running %s", sys._getframe())
        super()._update()

    def _start(self):
        logger.debug("Running %s", sys._getframe())
        super()._start()
        pass

    def _stop(self):
        logger.debug("Running %s", sys._getframe())
        super()._stop()
        pass

    def _remove(self):
        logger.debug("Running %s", sys._getframe())
        super()._remove()

    def install(self):
        logger.debug("Running %s", self.__class__.__qualname__)
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

    def remove(self):
        logger.debug("Running %s", sys._getframe())
        self._remove()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()
    logger.warning("Do not run this file directly. Start with rocm-install.py instead")
    logger.debug("what follows is just unit test output")
    testclass = ToolCliWrapperTestClass()
    logger.debug("Running test install")
    testclass.install()
    logger.debug("Running test configure")
    testclass.configure()
    logger.debug("Running test start")
    testclass.start()
    logger.debug("Running test stop")
    testclass.stop()
    logger.debug("Running test update")
    testclass.update()
    logger.debug("Running test remove")
    testclass.remove()
