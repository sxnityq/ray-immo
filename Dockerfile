FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -y

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-opencv \
    python3-setuptools \
    build-essential \
    libzmq3-dev \
    python3-pil \
    libsm6 \
    libxext6 \
    libxrender-dev \
    wget \
    git \
    unzip \
    ffmpeg \
    graphviz \
    openslide-tools

RUN pip install --upgrade pip \
    pip install jupyter jupyterlab

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--no-browser"]
