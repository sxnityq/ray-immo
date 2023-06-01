#!/bin/bash

# Install full TensorRT
apt-get install libnvinfer-lean8
apt-get install tensorrt -y
apt-get install uff-converter-tf -y
apt-get install onnx-graphsurgeon

python3 -m pip install numpy
python3 -m pip install numpy onnx
python3 -m pip install tensorflow
python3 -m pip install tensorflow_datasets
