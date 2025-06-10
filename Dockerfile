FROM python:3.12
LABEL authors="will liu"

# install CLI tools
RUN apt-get update && apt-get install -y \
    curl \
    aria2 \
    unzip

# s5cmd is a bit trickier - see https://github.com/peak/s5cmd/releases/tag/v2.3.0
RUN curl -L https://github.com/peak/s5cmd/releases/download/v2.3.0/s5cmd_2.3.0_Linux-64bit.tar.gz \
    | tar -xz -C /usr/local/bin s5cmd

WORKDIR /app

# install Python packages
COPY ./src/requirements.txt ./
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt
COPY src ./src


# change work dir to src - necessary for correct file writing
WORKDIR /app/src


