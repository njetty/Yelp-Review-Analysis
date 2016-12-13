#!/usr/bin/env bash

### Activate the virtual environment ###
virtualenv venv
source venv/bin/activate


### Install the requirement ###
pip install -r requirements.pip


mkdir input
mkdir input/Dataset
mkdir input/Dataset/Task1
mkdir input/Dataset/Task1/Results