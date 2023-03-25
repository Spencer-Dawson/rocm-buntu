#makes the rocm-buntu/tg folder if !exist and pulls the text-generation-webui repo from it

import os
import subprocess

class TGPuller:
    def __init__(self):
        self.WD = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'rocm-buntu'))
        self.TGPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tg'))
        self.TGREPO = "https://github.com/oobabooga/text-generation-webui.git"
    
    def pull(self):
        if not os.path.exists(self.TGPATH):
            os.makedirs(self.TGPATH)
        os.chdir(self.TGPATH)
        subprocess.run(["git", "clone", self.TGREPO])

if __name__ == "__main__":
    tgpuller = TGPuller()
    tgpuller.pull()
