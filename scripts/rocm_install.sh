#!/bin/bash

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
echo "1) ROCM 6.0"
echo "2) ROCm 5.7"
echo "3) ROCm 5.6"
echo "4) ROCm 5.5"
echo "5) ROCm 5.4"
echo "6) ROCm 5.3"
echo "7) ROCm 5.2"

read -p "Input> " rocm_version
rocm_version=${rocm_version:0:1}

# Convert rocm_version to the actual version number
if [ "$rocm_version" == "1" ]; then
    rocm_version="6.0"
elif [ "$rocm_version" == "2" ]; then
    rocm_version="5.7"
elif [ "$rocm_version" == "3" ]; then
    rocm_version="5.6"
elif [ "$rocm_version" == "4" ]; then
    rocm_version="5.5"
elif [ "$rocm_version" == "5" ]; then
    rocm_version="5.4"
elif [ "$rocm_version" == "6" ]; then
    rocm_version="5.3"
elif [ "$rocm_version" == "7" ]; then
    rocm_version="5.2"
else
    echo "Invalid choice. Exiting..."
    exit 1
fi

# make a tmp directory to install ROCm
mkdir -p /tmp/rocm || exit 1
cd /tmp/rocm || exit 1

sudo apt update || exit 1

if [ "$rocm_version" == "6.0" ]; then
    echo "Installing ROCm 6.0"
    wget https://repo.radeon.com/amdgpu-install/6.0/ubuntu/jammy/amdgpu-install_6.0.60000-1_all.deb || exit 1
    sudo sudo dpkg -i ./amdgpu-install_6.0.60000-1_all.deb || exit 1
elif [ "$rocm_version" == "5.7" ]; then
    echo "Installing ROCm 5.7"
    wget https://repo.radeon.com/amdgpu-install/5.7/ubuntu/jammy/amdgpu-install_5.7.50700-1_all.deb || exit 1
    sudo sudo dpkg -i ./amdgpu-install_5.7.50700-1_all.deb || exit 1
elif [ "$rocm_version" == "5.6" ]; then
    echo "Installing ROCm 5.6"
    wget https://repo.radeon.com/amdgpu-install/5.6/ubuntu/jammy/amdgpu-install_5.6.100-1236248_all.deb || exit 1
    sudo sudo dpkg -i ./amdgpu-install_5.6.100-1236248_all.deb || exit 1
elif [ "$rocm_version" == "5.5" ]; then
    echo "Installing ROCm 5.5"
    wget https://repo.radeon.com/amdgpu-install/5.5/ubuntu/jammy/amdgpu-install_5.5.100-1236248_all.deb || exit 1
    sudo sudo dpkg -i ./amdgpu-install_5.5.100-1236248_all.deb || exit 1
elif [ "$rocm_version" == "5.4" ]; then
    echo "Installing ROCm 5.4"
    wget https://repo.radeon.com/amdgpu-install/5.4.3/ubuntu/jammy/amdgpu-install_5.4.50403-1_all.deb || exit 1
    sudo sudo dpkg -i ./amdgpu-install_5.4.50403-1_all.deb || exit 1
elif [ "$rocm_version" == "5.3" ]; then
    echo "Installing ROCm 5.3"
    wget https://repo.radeon.com/amdgpu-install/5.3/ubuntu/jammy/amdgpu-install_5.3.50300-1_all.deb || exit 1
    sudo sudo dpkg -i ./amdgpu-install_5.3.50300-1_all.deb || exit 1
elif [ "$rocm_version" == "5.2" ]; then
    echo "Installing ROCm 5.2"
    wget https://repo.radeon.com/amdgpu-install/22.20.1/ubuntu/bionic/amdgpu-install_22.20.50201-1_all.deb || exit 1
    sudo sudo dpkg -i ./amdgpu-install_22.20.50201-1_all.deb || exit 1
fi

# ensure amdgpu-install is configured properly for ROCm usecase
sudo amdgpu-install --usecase=hiplibsdk,hip,rocm,dkms

# cleanup tmp files
cd ~
rm -rf /tmp/rocm

sudo usermod -a -G video $USER
sudo usermod -a -G render $USER

echo "Installation complete. Reboot your system to complete the installation."