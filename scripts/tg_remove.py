# uninstalls text-generation-webui

import os
import subprocess
import shutil

class TGRemover:
    def __init__(self):
        self.WD = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'rocm-buntu'))
        self.TGPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tg'))

    def remove(self):
        if os.path.exists(self.TGPATH):
            shutil.rmtree(self.TGPATH)

if __name__ == "__main__":
    remover = TGRemover()
    remover.remove()