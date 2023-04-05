"""
util functions for downloading files
"""

import os
import sys
import subprocess
import logging
import requests
import zipfile
import tarfile
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_file(url, path, overwrite= False, filename=None):
    """
    Downloads a file from a url to a path
    :param url: url to download from
    :param path: path to download to
    :param overwrite: if True the file will be overwritten if it already exists
    :param filename: name of the file to download if None the filename will be the default filename
    """
    def get_filename_from_url(url):
        return url.split('/')[-1]
    logger.debug("Downloading file from %s to %s" % (url, path))
    if filename is None:
        filename = get_filename_from_url(url)
    filepath = path + filename
    if not os.path.exists(filepath) or overwrite:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        # f.flush()
        logger.debug("Downloaded file from %s to %s" % (url, path))
    else:
        logger.debug("File %s already exists, not downloading" % filepath)

def download_file_civitai_api(url, path, overwrite= False):
    """
    Downloads a file from a url to a path
    :param url: url to download from
    :param path: path to download to
    :param overwrite: if True the file will be overwritten if it already exists
    """
    # civitai docs for reference: https://github.com/civitai/civitai/wiki/REST-API-Reference
    # civitai download reference: wget https://civitai.com/api/download/models/{modelVersionId} --content-disposition
    # relies on wget being installed :( I'm sure there is a better way to do this, but I can't be bothered
    logger.debug("Downloading file from %s to %s" % (url, path))
    if not os.path.exists(path):
        raise Exception("Path %s does not exist" % path)
    # downloading to a specific path with wget seems to be a bit of a pain so it's easier to just change the working directory
    os.chdir(path)
    if overwrite:
        spoc = subprocess.Popen(["wget", url, "--content-disposition", "--no-verbose", "--show-progress"])
        spoc.wait()
    else:
        spoc = subprocess.Popen(["wget", "--no-clobber", url, "--content-disposition", "--no-verbose", "--show-progress"])
        spoc.wait()
