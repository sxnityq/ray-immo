#!/bin/bash

apt-get update
apt-get install -y wget gnupg2 software-properties-common

wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin \
    && mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub \
    && apt-key add 7fa2af80.pub
echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64 /" >> /etc/apt/sources.list.d/cuda.list

apt-get update
apt-get install -y --no-install-recommends \
    libcudnn8=8.9.1.23-1+cuda12.1 \
    libcudnn8-dev=8.9.1.23-1+cuda12.1 \
    libcudnn8-samples=8.9.1.23-1+cuda12.1

cp -r /usr/src/cudnn_samples_v8/ $HOME
