FROM --platform=linux/amd64 python:3.10-slim

RUN apt-get update && \
    apt-get install -y \
    git gcc g++ python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/list/*

# Install poetry
RUN pip install poetry

# Create directory structure and copy files
WORKDIR /opt/mypackage
ARG CACHEBUST=1
COPY . /opt/mypackage/autoafids_prep
# RUN git clone -b djay/registration https://github.com/afids/autoafids_prep.git

# Install the pipeline.
WORKDIR /opt/mypackage/autoafids_prep
RUN poetry install --no-dev && \
    poetry cache clear pypi --all

# Run the pipeline
# ENTRYPOINT [ "/bin/bash", "-c" ]
ENTRYPOINT ["poetry","run","autoafids_prep"]