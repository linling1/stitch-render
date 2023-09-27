FROM ubuntu:22.04

RUN apt-get update && apt-get install -y wget unzip libvips-dev libdrm2 libice6 libsm6 libgbm-dev libxkbcommon-x11-0 libgtk-3-0 libasound2

RUN wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash && source ~/.bashrc && nvm install 16

RUN echo y | npm install @puppeteer/browsers

# RUN wget "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1119062%2Fchrome-linux.zip?generation=1679170252447036&alt=media" --no-check-certificate -q -O chrome.zip && unzip chrome.zip

RUN npx @puppeteer/browsers install chrome@113.0.5672.63

RUN curl https://sh.rustup.rs -sSf > rustup-init.sh && sh rustup-init.sh -y && source "$HOME/.cargo/env"
