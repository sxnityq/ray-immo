#!/bin/bash

wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin

mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
apt-get update

apt-get install libcudnn8=8.9.1.23-1+12.1
apt-get install libcudnn8-dev=8.9.1.23-1+12.1
apt-get install libcudnn8-samples=8.9.1.23-1+12.1

#cp -r /usr/src/cudnn_samples_v8/ $HOME
#cd  $HOME/cudnn_samples_v8/mnistCUDNN
#make clean && make
#./mnistCUDNN