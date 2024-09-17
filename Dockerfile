FROM --platform=linux/amd64 python:3.10-slim

RUN apt-get update && \
    apt-get install -y \
    git gcc g++ python3-dev wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/list/*

# Download and configure Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

# Update PATH environment variable
ENV PATH /opt/conda/bin:$PATH

RUN conda create -n myenv python=3.10 -y \
    && conda clean --all --yes

# Create a conda environment and install ITK
RUN /bin/bash -c "conda init && source ~/.bashrc && conda activate myenv && conda install -c conda-forge itk -y"

# Set environment variables
ENV PATH /opt/conda/envs/myenv/bin:$PATH

RUN pip install poetry

# Clone and install package
RUN mkdir -p /opt/my-package && mkdir /opt/my-package/bids_dataset && mkdir /opt/my-package/output
WORKDIR /opt/my-package
RUN git clone -b djay/registration https://github.com/afids/autoafids_prep.git

# Add antspyx FOR NOW!
RUN /bin/bash -c "source ~/.bashrc && cd ./autoafids_prep && poetry install"
WORKDIR /opt/my-package/autoafids_prep

# Expose the entrypoint to run the pipeline
ENTRYPOINT ["poetry","run","autoafids_prep"]