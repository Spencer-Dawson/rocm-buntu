#reads a yaml config file and configures text-generation-webui based on that configuration
import os
import sys
import subprocess
from ..utils.confighelpers import read_config

class TGConfigurator:
    def __init__(self, configfilepath, defaultconfigfilepath, tgexec, tgenv):
        #verify that the paths are absolute
        if not os.path.isabs(configfilepath):
            raise Exception("configfilepath is not absolute")
        if not os.path.isabs(defaultconfigfilepath):
            raise Exception("defaultconfigfilepath is not absolute")
        if not os.path.isabs(tgexec):
            raise Exception("tgexec is not absolute")
        if not os.path.isabs(tgenv):
            raise Exception("tgenv is not absolute")

        self.CONFIGFILEPATH = configfilepath
        self.DEFAULTCONFIGFILEPATH = defaultconfigfilepath
        self.TGEXEC = tgexec
        self.TGENV = tgenv

        print("CONFIGFILEPATH: " + self.CONFIGFILEPATH)
        print("DEFAULTCONFIGFILEPATH: " + self.DEFAULTCONFIGFILEPATH)
        print("TGEXEC: " + self.TGEXEC)
        print("TGENV: " + self.TGENV)

    def configure(self):
        #if config contains values under models -> huggingface -> modelname download those
        config = read_config(self.CONFIGFILEPATH, self.DEFAULTCONFIGFILEPATH)
        os.chdir(self.TGEXEC)
        if 'models' in config:
            if 'huggingface' in config['models']:
                #config['models']['huggingface'] is either a model name itself or a list of model names this handles both cases
                if isinstance(config['models']['huggingface'], str):
                    config['models']['huggingface'] = [config['models']['huggingface']]
                for modelname in config['models']['huggingface']:
                    print("Downloading model %s" % modelname)
                    #using subprocess to run the command from the virtual environment
                    sproc =subprocess.Popen([self.TGENV+'python', 'download-model.py', modelname])
                    sproc.wait()


        else:
            print("No models specified in config file")

if __name__ == "__main__":
    tgconfigurator = TGConfigurator()
    tgconfigurator.configure()
