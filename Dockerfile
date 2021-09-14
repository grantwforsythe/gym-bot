FROM ubuntu:20.04

ENV EMAIL=your-email@gmail.com
ENV PASSWORD=your-password
ENV DRIVER=/usr/local/bin/geckodriver

RUN apt update \
    && apt install -y wget firefox 

# install geckodriver and firefox
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz \
    && tar -zxf geckodriver* -C /usr/local/bin \
    && chmod +x /usr/local/bin/geckodriver \
    && rm geckodriver*

RUN mkdir gym-bot && cd gym-bot
WORKDIR gym-bot
COPY .

# set up python environment and run bot
RUN python3 -m venv venv \
    && source venv\bin\activate \
    && pip3 install -r requirements.txt \
    && python3 -m bot
