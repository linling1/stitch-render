FROM ubuntu:20.04

RUN apt-get update && echo 12 | DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y wget unzip libvips-dev libdrm2 libice6 libsm6 libgbm-dev libxkbcommon-x11-0 libgtk-3-0 libasound2 curl python3.8 python3-pip ffmpeg
# RUN apt-get install -y tesseract-ocr


ENV HOME /root
ENV NODE_VERSION 20.15.0
ENV NVM_DIR $HOME/.nvm

RUN wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash 
SHELL ["/bin/bash","-ic"] 
RUN source ~/.bashrc && nvm install $NODE_VERSION && nvm use $NODE_VERSION

RUN echo y | npx @puppeteer/browsers install chrome@126.0.6478.126
RUN ln -s /chrome/linux-126.0.6478.126/chrome-linux64/chrome /usr/bin/google-chrome

    
COPY . /spider-stitch-render

WORKDIR /spider-stitch-render


RUN pip3 install -r requirements.txt

# RUN mkdir -p ~/.cache/whisper/ && wget https://openaipublic.azureedge.net/main/whisper/models/d3dd57d32accea0b295c96e26691aa14d8822fac7d9d27d5dc00b4ca2826dd03/tiny.en.pt && mv tiny.en.pt ~/.cache/whisper/
RUN mkdir -p ~/.cache/whisper/ && wget https://openaipublic.azureedge.net/main/whisper/models/25a8566e1d0c1e2231d1c762132cd20e0f96a85d16145c3a00adf5d1ac670ead/base.en.pt && mv base.en.pt ~/.cache/whisper/

RUN python3 -m api.api --workers=5