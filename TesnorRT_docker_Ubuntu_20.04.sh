#!/bin/bash

# Install full TensorRT
apt-get install libnvinfer-lean8
apt-get install tensorrt
apt-get install libnvinfer-vc-plugin8
apt-get install python3-libnvinfer-dispatch
apt-get install python3-libnvinfer-devpython3 -m pip install protobuf
apt-get install uff-converter-tf
apt-get install onnx-graphsurgeon

python3 -m pip install numpy
python3 -m pip install numpy onnx
python3 -m pip install tensorflow
python3 -m pip install tensorflow_datasets
