FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -y

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-opencv

RUN pip install --upgrade pip \
    pip install -r requirements.txt \
    pip install jupyter jupyterlab


RUN sh bash_commands/TensorRT_docker_Ubuntu_20.04.sh


EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--no-browser"]
