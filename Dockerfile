FROM ubuntu:16.04
RUN apt-get update && apt-get install -y \
     apt-transport-https \ 
     python3 \
     python3-pip \
     && pip3 install --upgrade pip \
     && rm -rf /var/lib/apt/lists/*

# set the working directory for containers
WORKDIR  /usr/src/House_Price

# Copy all the files from the project’s root to the working directory
COPY $path /usr/src/House_Price/ 
RUN ls -la /usr/src/House_Price/*

# Installing python dependencies
RUN pip3 install --no-cache-dir -r /usr/src/House_Price/requirements.txt