# reads a yaml config file and configures stable-diffusion-webui based on that configuration
import os
import sys
import subprocess
from ..utils.confighelpers import read_config
from ..utils import downloadhelper
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("SDConfigurator")

class SDConfigurator:
    def __init__(self, configfilepath, defaultconfigfilepath, sdexec, sdenv):
        #verify that the paths are absolute
        if not os.path.isabs(configfilepath):
            raise Exception("configfilepath is not absolute")
        if not os.path.isabs(defaultconfigfilepath):
            raise Exception("defaultconfigfilepath is not absolute")
        if not os.path.isabs(sdexec):
            raise Exception("sdexec is not absolute")
        if not os.path.isabs(sdenv):
            raise Exception("sdenv is not absolute")

        self.CONFIGFILEPATH = configfilepath
        self.DEFAULTCONFIGFILEPATH = defaultconfigfilepath
        self.SDEXEC = sdexec
        self.SDENV = sdenv

    def configure(self):
        config = read_config(self.CONFIGFILEPATH, self.DEFAULTCONFIGFILEPATH)
        logger.debug(config)
        os.chdir(self.SDEXEC)
        if 'embeddings' in config:

            if 'civitai' in config['embeddings']:
                #config['embeddings']['civitai'] is either a model name itself or a list of model names this handles both cases
                if isinstance(config['embeddings']['civitai'], str):
                    config['embeddings']['civitai'] = [config['embeddings']['civitai']]
                for embedding in config['embeddings']['civitai']:
                    logger.info("Downloading embedding %s to %s", embedding, self.SDEXEC + "embeddings/")
                    downloadhelper.download_file_civitai_api(embedding, self.SDEXEC + "embeddings/")
        if 'models' in config:
            if 'hypernetworks' in config['models']:
                #config['models']['hypernetworks']['civitai'] is either a model name itself or a list of model names this handles both cases
                if isinstance(config['models']['hypernetworks']['civitai'], str):
                    config['models']['hypernetworks']['civitai'] = [config['models']['hypernetworks']['civitai']]
                for hypernetwork in config['models']['hypernetworks']['civitai']:
                    logger.info("Downloading model %s to %s", hypernetwork, self.SDEXEC + "models/hypernetworks/")
                    downloadhelper.download_file_civitai_api(hypernetwork, self.SDEXEC + "models/hypernetworks/")
            if 'Stable-diffusion' in config['models']:
                #config['models']['Stable-diffusion']['civitai'] is either a model name itself or a list of model names this handles both cases
                if isinstance(config['models']['Stable-diffusion']['civitai'], str):
                    config['models']['Stable-diffusion']['civitai'] = [config['models']['Stable-diffusion']['civitai']]
                for modelname in config['models']['Stable-diffusion']['civitai']:
                    logger.info("Downloading model %s to %s", modelname, self.SDEXEC + "models/Stable-diffusion/")
                    downloadhelper.download_file_civitai_api(modelname, self.SDEXEC + "models/Stable-diffusion/")
            if 'Lora' in config['models']:
                #config['models']['Lora']['civitai'] is either a model name itself or a list of model names this handles both cases
                if isinstance(config['models']['Lora']['civitai'], str):
                    config['models']['Lora']['civitai'] = [config['models']['Lora']['civitai']]
                for lora in config['models']['Lora']['civitai']:
                    logger.info("Downloading lora %s to %s", lora, self.SDEXEC + "models/Lora/")
                    downloadhelper.download_file_civitai_api(lora, self.SDEXEC + "models/Lora/")
