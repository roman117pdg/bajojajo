FROM python:3.6

EXPOSE 21037/UDP
EXPOSE 5000

LABEL Mikolaj Rogacki

# prerequisites needed for pocketspihnx installation 
# Source: https://raw.githubusercontent.com/WuganAa/docker-pocketsphinx/master/Dockerfile
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-pip \
    build-essential \
    swig \ 
    libpulse-dev \ 
    libasound2-dev \ 
    software-properties-common \
    zip \
    unzip \
    yasm \
    libtbb2 \
    libtbb-dev \
    libpng-dev \
    libtiff-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*



RUN pip3 install --upgrade pip
RUN pip3 install pocketsphinx
RUN pip3 install sockets
RUN pip3 install flask
RUN pip3 install qrcode[pil]
RUN pip3 install transformers[torch]
RUN pip3 install sentencepiece


ADD server.py /home/ietk/app/server.py
ADD speech2text.py /home/ietk/app/speech2text.py
ADD sockets.py /home/ietk/app/sockets.py
ADD logger.py /home/ietk/app/logger.py
ADD flask_qr.py /home/ietk/app/flask_qr.py
# ADD flask_api.py /home/ietk/app/flask_api.py
ADD translator.py /home/ietk/app/translator.py
ADD templates/login.html /home/ietk/app/templates/login.html

# CMD [ "python", "-u", "/home/ietk/app/flask_api.py" ]
CMD [ "python", "-u", "/home/ietk/app/flask_qr.py" ]
