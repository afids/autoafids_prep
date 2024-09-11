# Anatomical Fiducials (AFIDs) Data Processing Pipeline 
AIMS Lab Research Team at the Robarts Research Institute - 2023-2024


*This package is under active development. It should be stable and reproducible, but please let any of the active contributing members know if there are any bugs or unusual behaviour.*

This Python package is a data processing pipeline based on Snakemake and SnakeBIDS workflow management tools to prepare data for a Convolutional Neural Network (CNN) deep learning model [afids-CNN](https://github.com/afids/afids-CNN). Since AFIDS-CNN is under active development, this package contains tunable parameters that are not normally exposed in a data processing pipeline; the user is highly encourage to read docstrings and get familiar with the relevant workflow managements tools prior to using this software. Likewise, there may be frequent updates to this package as the project matures (see the [changelog](CHANGELOG.md) for more details).

## Brief Overview of the Pipeline
1. Performs rigid registration (i.e., 6 d.o.f) from MNI template to Native space.
2. Conformes images to a desired isotropic resolution (default: 1mm). 
3. Executes image intensity normalization by various supported algorithms (default: min-max normalization).

## Table of Contents
1. [Installation](#installation)
2. [Getting the datasets](#getting-the-datasets)
3. [Quick Guide](#quick-guide) 
4. [Known issues](#known-issues)
5. [Roadmap](#roadmap)
6. [Questions, Issues, Suggestions, and Other Feedback](#questions--issues)

## Installation

### Installing Poetry
We use poetry tool for dependency management and to package the python project. You can find step by step instructions on how to install it by visiting it's official [website](https://python-poetry.org/docs/).

### Local Installation

After installing poetry, clone this repository via:

```bash
git clone https://github.com/afids/autoafids_prep.git
```

You can then install the python package using one of the following commands, which should be executed within the repository folder (i.e., autoafids_prep/).

To install the autoafids_prep package "normally", use:

```bash
poetry install
```
If you want to install in _develop mode_, use:

```bash
poetry install -e
```

To activate the virtual environment, use:

```bash
poetry shell
```

## Getting the datasets
All the datasets mentioned below have been deposited at DOI-issuing repositories separately and follow the BIDS directory hierarchy. To download them, follow the links:

1. [100 Unrelated Human Connectome Project (AFIDs-HCP)](https://zenodo.org/records/8072105) - You'll need to be authenticated before you can download this dataset. Please contact Alaa Taha for the required access code. 
2. [Open Access Series of Imaging Studies (AFIDs-OASIS)](https://zenodo.org/records/7641090)
3. [The Stereotactic Neurosurgery (SNSX) dataset](https://openneuro.org/datasets/ds004470/versions/1.0.0)
4. [The London Health Sciences Center Parkinson’s disease (LHSCPD) dataset](https://openneuro.org/datasets/ds004471/versions/1.0.0)

## Quick Guide
To display help information about the `autoafids_prep` program, use:

```
autoafids_prep -h
```

To execute a dry-run of the workflow, use:

```
autoafids_prep path/to/dataset path/to/dataset/derivatives participant --cores 1 -np --force-output
```
## Known Issues
- Niftyreg is a registration software that is required to run the pipeline but it's not installed along with the `autoafids_prep` package. On the CBS server, it comes pre-installed but a user testing on their local machine would need to install it manually. We can either add a section in the README on how to install it manually for local testing or alert users to work on the CBS server.
- Currently, the slow and medium flags in the pipeline are under development.

## Roadmap
Here are some future plans for `autoafids_prep`:
- Synchronize the pipeline with [AFIDS-CNN](https://github.com/afids/afids-CNN) to avoid latency between downloading the datasets and preparing them for training the model. 
- Might be worth exploring docker containerizing the pipeline. 

## Questions, Issues, Suggestions, and Other Feedback
Please reach out if you have any questions, suggestions, or other feedback related to this software—either through email (dbansal7@uwo.ca) or the discussions page. Larger issues or feature requests can be posted and tracked via the issues page. Finally, you can also reach out to Alaa Taha, the Science Lead for autoafids_prep.
