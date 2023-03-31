#makes the passed in full path if !exist and pulls the passed in repo from it

import os
import subprocess
import argparse

class GitPuller:
    def __init__(self, repo, path):
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
        print("Path: " + self.PATH)
        print("Repo: " + self.REPO)

    def pull(self):
        #make the passed in full path if !exist
        if not os.path.exists(self.PATH):
            print("making directory " + self.PATH)
            os.makedirs(self.PATH)
        os.chdir(self.PATH)
        #print the current working directory
        print("Current working directory: " + os.getcwd())
        subprocess.run(["git", "clone", self.REPO])

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    #full path to the folder to pull the repo into
    argparser.add_argument("path", help="path to the folder to pull the repo into")
    #repo to pull
    argparser.add_argument("repo", help="repo to pull")
    args = argparser.parse_args()
    fullpath = os.path.abspath(args.path)
    tgpuller = GitPuller(args.repo, fullpath)
    tgpuller.pull()
