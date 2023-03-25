#!/bin/bash

echo "This script is completely untested. "
echo "It's more intended as a general overview of what needs to be done to install ROCm on Ubuntu 22.04 then as an actual installer. "
echo "Use at your own risk. And provide feedback if you have suggested fixes. "

# make sure user wants to continue
read -p "Do you want to continue? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

#install rocm in ubuntu 22.04
# see https://docs.amd.com/bundle/ROCm-Installation-Guide-v5.3/page/How_to_Install_ROCm.html for reference

# Check if the system is running Ubuntu 22.04
if [ "$(lsb_release -rs)" != "22.04" ]; then
    echo "This script is only for Ubuntu 22.04"
    exit 1
fi

# Check for ROCm supported gpu
# todo: check for supported gpu using lspci and grep
if [ "$(lspci | grep -i 'AMD' | grep -i 'Radeon')" == "" ]; then
    echo "No supported AMD GPU found. Exiting..."
    exit 1
fi

# Ask user to specify the version of ROCm to install
echo "Which version of ROCm do you want to install?"
echo "1) ROCm 5.4"
echo "2) ROCm 5.3"

read -p "Input> " rocm_version
rocm_version=${rocm_version:0:1}

# Convert rocm_version to the actual version number
if [ "$rocm_version" == "1" ]; then
    rocm_version="5.4"
elif [ "$rocm_version" == "2" ]; then
    rocm_version="5.3"
else
    echo "Invalid choice. Exiting..."
    exit 1
fi

# make a tmp directory to install ROCm
mkdir -p /tmp/rocm || exit 1
cd /tmp/rocm || exit 1

sudo apt update || exit 1

# Install ROCm5.4 if user specified
if [ "$rocm_version" == "5.4" ]; then
    echo "Installing ROCm 5.4"
    wget https://repo.radeon.com/amdgpu-install/5.4.3/ubuntu/jammy/amdgpu-install_5.4.50403-1_all.deb || exit 1
    sudo apt-get install ./amdgpu-install_5.4.50403-1_all.deb || exit 1

fi

# Install ROCm5.3 if user specified
if [ "$rocm_version" == "5.3" ]; then
    echo "Installing ROCm 5.3"
    wget https://repo.radeon.com/amdgpu-install/5.3/ubuntu/jammy/amdgpu-install_5.3.50300-1_all.deb || exit 1
    sudo apt install ./amdgpu-install_5.3.50300-1_all.deb || exit 1
    exit 1
fi

# ensure amdgpu-install is configured properly for ROCm usecase
sudo amdgpu-install --usecase=hiplibsdk,hip,rocm,dkms

# cleanup tmp files
cd ~
rm -rf /tmp/rocm

sudo usermod -a -G video $USER
sudo usermod -a -G render $USER

echo "Installation complete. Reboot your system to complete the installation."