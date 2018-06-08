# Pull base image.
FROM ubuntu:18.04

# Install.
RUN \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get -y install sqlite && \
  apt-get install -y sqlite && \
  apt-get install -y python3 && \
  apt-get install -y python3-pip && \
  rm -rf /var/lib/apt/lists/*

# Add files.
ADD eas /root/eas
ADD requirements*txt /root/
ADD run.py /root/

RUN pip3 install -r /root/requirements.txt
# Set environment variables.
ENV HOME /root

# Define working directory.
WORKDIR /root

# Set a temporary fake SENTRY_DSN env variable
ENV SENTRY_DSN https://cafecafecaffeebeeff@sentry.io/12055

# Define default command.
CMD /usr/bin/python3 run.py
