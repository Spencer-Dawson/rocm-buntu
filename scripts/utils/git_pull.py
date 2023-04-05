import os
import subprocess
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitPuller:
    """
    makes the passed in full path if !exist and pulls the passed in repo from it
    """
    def __init__(self, repo, path):
        """
        sets variables used in pull()
        repo: a string of the repo url
        path: a string of the full path to pull the repo to
        """
        #check if path is a full path string
        if not os.path.isabs(path):
            raise ValueError("path must be a full path string")
        #check if repo is a string
        if not isinstance(repo, str):
            raise ValueError("repo must be a string")
        #check if repo is a valid github repo
        if "github.com" not in repo:
            raise ValueError("repo must be a valid github repo")
        self.PATH = path
        self.REPO = repo
        # REPOPATH comes fromthe last part of the repo url
        self.REPOPATH = os.path.abspath(os.path.join(path, self.REPO.split("/")[-1]))
        logger.debug("Path: " + self.PATH)
        logger.debug("Repo: " + self.REPO)

    def pull(self):
        """
        pulls the git repository
        """
        #make the passed in full path if !exist
        if not os.path.exists(self.PATH):
            logger.info("making directory " + self.PATH)
            os.makedirs(self.PATH)
        os.chdir(self.PATH)
        #print the current working directory
        logger.debug("Current working directory: " + os.getcwd())
        subprocess.run(["git", "clone", self.REPO])

if __name__ == "__main__":
    """
    Imports? We don't need no stinking imports!
    callable as a cli tool if that's your thing
    """
    argparser = argparse.ArgumentParser()
    #full path to the folder to pull the repo into
    argparser.add_argument("path", help="path to the folder to pull the repo into")
    #repo to pull
    argparser.add_argument("repo", help="repo to pull")
    args = argparser.parse_args()
    fullpath = os.path.abspath(args.path)
    tgpuller = GitPuller(args.repo, fullpath)
    tgpuller.pull()
