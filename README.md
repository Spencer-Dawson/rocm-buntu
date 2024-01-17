# rocm-buntu
AI toolkit in a box for AMD GPU owners on Ubuntu 22.04. This project is designed to make installation, removal, use, upgrading, and configuring rapidly developing local ai tools simple for AMD Linux power users.

THIS SOFTWARE IS PREALPHA

Features:
- AMD ROCm support via rocm python cli tool
    - Supports ROCm Installation
- oogabooga/text-generation-webui support via tg python cli tool
    - Supports Installation
    - Supports starting either as a daemon or as a subprocess
    - Supports stopping as a daemon
    - Supports configuration step which automatically downloads specified models from huggingface, starting as and stopping and remove oogabooga/text-generation-webui using tg python api
    - supports uninstallation(deletes installation folder and virtual environment)
- Supports AUTOMATIC1111/stable-diffusion-webui cia sd python cli tool
    - Supports Installation
    - Supports starting as either a daemon or as a subprocess
    - Supports stopping as a daemon

Coming Soon:
- text-generation-webui improvements
    - Will integrate Bits-And-Bytes ROCm Build/install
    - Will enable installation of 4 bit models
- stable-diffusion-webui improvements
    - Will enable user configuration based installation of models, etc from civitai
- Will integrate other tools based on feedback

Support for other environments(Besides Ubuntu 22.04 with AMD ROCm compatible GPUs) is not currently being pursued, but may considered in the future

Instalation:
- install git, python3 virtualenv, and python3-setuptools, python3-dev, libstdc++-12-dev '''sudo apt install git python3-venv python3-setuptools python3-dev libstdc++-12-dev'''
- From your own folder(or any other directory you want to download under that doesn't have a space in the folder path)
    - '''git clone https://github.com/Spencer-Dawson/rocm-buntu.git'''
    - '''cd rocm-buntu'''
    - To install rocm run '''./rocm.py install''' I strongly recommend using the latest version of rocm
    - Reboot your system
    - To install text-generation-webui run '''./tg.py install'''
    - To install stable-diffusion-webui run '''./sd.py install'''
