FROM ubuntu:20.04

RUN apt-get update && echo 12 | DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install -y wget unzip libvips-dev libdrm2 libice6 libsm6 libgbm-dev libxkbcommon-x11-0 libgtk-3-0 libasound2 curl python3.8 python3-pip


ENV HOME /root
ENV NODE_VERSION 20.15.0
ENV NVM_DIR $HOME/.nvm

RUN wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash 
SHELL ["/bin/bash","-ic"] 
RUN source ~/.bashrc && nvm install $NODE_VERSION && nvm use $NODE_VERSION

RUN echo y | npx @puppeteer/browsers install chrome@126.0.6478.126
RUN ln -s /chrome/linux-126.0.6478.126/chrome-linux64/chrome /usr/bin/google-chrome


RUN wget https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz -O ffmpeg.tar.xz && \
    tar -xf ffmpeg.tar.xz && \
    rm ffmpeg.tar.xz
RUN cp ffmpeg-*-linux64-gpl/bin/ffmpeg /usr/local/bin/ && \
    rm -rf ffmpeg-*

    
COPY . /spider-stitch-render

WORKDIR /spider-stitch-render


RUN pip3 install -r requirements.txt

RUN python3 -m api.api --workers=5