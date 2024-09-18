FROM --platform=linux/amd64 python:3.10-slim

RUN apt-get update && \
    apt-get install -y \
    git gcc g++ python3-dev wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/list/*

# # Download and configure Miniconda
# RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
#     bash miniconda.sh -b -p /opt/conda && \
#     rm miniconda.sh

# # Update PATH environment variable
# ENV PATH /opt/conda/bin:$PATH

# # Create virtual environment
# RUN conda create -n myenv python=3.10 -y \
#     && conda clean --all --yes

# # Activate the conda environment and install ITK
# RUN /bin/bash -c "conda init && source ~/.bashrc && conda activate myenv && conda install -c conda-forge itk -y"

# # Set environment variables
# ENV PATH /opt/conda/envs/myenv/bin:$PATH

# Install poetry
RUN pip install poetry

# Create directory structure and copy files
# COPY poetry.lock pyproject.toml /opt/mypackage/autoafids_prep/
# COPY autoafids_prep /opt/mypackage/autoafids_prep/autoafids_prep
WORKDIR /opt/mypackage
ARG CACHEBUST=1
COPY . /opt/mypackage/autoafids_prep
# RUN git clone -b djay/registration https://github.com/afids/autoafids_prep.git

# Install the pipeline.
RUN /bin/bash -c "source ~/.bashrc && cd /opt/mypackage/autoafids_prep && poetry install"
WORKDIR /opt/mypackage/autoafids_prep

# Run the pipeline
# ENTRYPOINT [ "/bin/bash", "-c" ]
ENTRYPOINT ["poetry","run","autoafids_prep"]