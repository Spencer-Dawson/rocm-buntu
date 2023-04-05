"""
confighelpers

A collection of functions for reading and writing config files

"""
#used as an import by other scripts
#returns a dictionary of the config file

import os
import sys
import shutil
import yaml
import logging

logging.basicConfig(level=logging.info)
logger = logging.getLogger(__name__)

def read_config(configfilename, defaultconfigfilename = None):
    """
    Takes a filename and returns a dictionary of the config file
    If defaultconfigfilename is specified and the config file does not exist, it will be overwritten with the default config file
    """
    #ensure configfilename is an absolute path
    if not os.path.isabs(configfilename):
        raise Exception("configfilename is not absolute")
    if defaultconfigfilename is not None:
        #ensure defaultconfigfilename is an absolute path
        if not os.path.isabs(defaultconfigfilename):
            raise Exception("defaultconfigfilename is not absolute")

    #check if config file exists and if not try overwriting it with the default config file
    if not os.path.isfile(configfilename):
        if defaultconfigfilename is not None:
            logger.info("Config file %s does not exist, overwriting with default config file %s" % (configfilename, defaultconfigfilename))
            try:
                shutil.copyfile(defaultconfigfilename, configfilename)
            except:
                logger.critical("Default config file %s does not exist" % defaultconfigfilename)
                sys.exit(1)
    if os.path.isfile(configfilename):
        #read config file
        with open(configfilename, 'r') as f:
            config = yaml.safe_load(f)
            return config
    else:
        logger.critical("Config file %s does not exist" % configfilename)
        sys.exit(1)
