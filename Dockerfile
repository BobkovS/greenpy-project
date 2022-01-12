FROM python:3.6.6-slim

WORKDIR /home/greenpy

RUN mkdir -p /home/greenpy/workdir

RUN apt-get update
RUN apt-get install -y locales
RUN locale-gen --purge en_US.UTF-8
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN apt-get install -y gcc && apt-get install -y g++

RUN python -m venv venv
RUN . venv/bin/activate

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt; exit 0
RUN pip install gevent==1.2.0
RUN pip install gunicorn==19.9.0

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY app app
COPY git.properties greenpy.py config.py boot.sh ./

RUN chmod a+x boot.sh

ENV FLASK_APP greenpy.py

RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "nano"]

EXPOSE 8080
ENTRYPOINT ["./boot.sh"]