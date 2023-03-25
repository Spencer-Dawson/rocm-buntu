#reads a yaml config file and configures text-generation-webui based on that configuration
import os
import sys
import subprocess
from .utils.configreader import read_config

class TGConfigurator:
    def __init__(self):
        self.WD = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'rocm-buntu'))
        self.CONFIGFILEPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config', 'tg-user.yml'))
        self.DEFAULTCONFIGFILEPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config', 'tg-default.yml'))
        self.TGPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tg'))
        self.TGEXEC = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tg', 'text-generation-webui'))
        self.TGENV = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tg', 'venv', 'bin'))
    
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
                    sproc =subprocess.Popen([self.TGENV+'/python', 'download-model.py', modelname])
                    sproc.wait()
                    

        else:
            print("No models specified in config file")

if __name__ == "__main__":
    tgconfigurator = TGConfigurator()
    tgconfigurator.configure()