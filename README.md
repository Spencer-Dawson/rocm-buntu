# rocm-buntu
AI toolkit in a box for AMD GPU owners on Ubuntu 22.04. This project is designed to make instalation, removal, use, upgrading, and configuring rapidly developing local ai tools simple for AMD Linux power users.

THIS SOFTWARE IS PREALPHA

Features:
- AMD ROCm support via rocm python cli tool
    - Supports ROCm Installation
- oogabooga/text-generation-webui support via tg python cli tool
    - Supports Instalation
    - Starting either as a daemon or as a subprocess
    - Supports stopping as a daemon
    - Supports configuration step which automatically downloads specified models from huggingface, starting as and stopping and remove oogabooga/text-generation-webui using tg python api
    - supports uninstallation(deletes installation folder and virtual environment)

Coming Soon:
- Will integrate Bits-And-Bytes ROCm Build/install into tg
- Will refactor tg scripts
- Will integrate AUTOMATIC1111/stable-diffusion-webui with it's own api
    - user configuration based installation of models, etc from civitai already planned for
- Will integrate other tools based on feedback

Support for other environments(Besides Ubuntu 22.04 with AMD ROCm compatible GPUs) is not currently being pursued, but may considered in the future
