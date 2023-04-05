# install AMD ROCm on Ubuntu 22.04
# todo add support for removal, update, and configure
# todo check for existing installation

import argparse
import subprocess
from baseclass import PackageManagerBaseClass
import logging

logger = logging.getLogger(__name__)

class Rocm(PackageManagerBaseClass):
    def __init__(self):
        super().__init__("rocm")

    def _pull(self):
        super()._pull()

    def _preinstall(self):
        super()._preinstall()

    def _install(self):
        #call scripts/rocm_install.sh
        subprocess.run(["./scripts/rocm_install.sh"])

    def _postinstall(self):
        super()._postinstall()

    def _configure(self):
        super()._configure()

    def _update(self):
        super()._update()

    def _remove(self):
        return super()._remove()

    def install(self):
        self._install()

    def remove(self):
        self._remove()

    def update(self):
        self._update()

    def configure(self):
        self._configure()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['install', 'remove', \
                                            'update', 'configure'])
    parser.add_argument('extra_args', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    # run command
    rocm = Rocm()
    if args.command == "install":
        rocm.install()
