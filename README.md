# dsti_mlops_labs

## Overview
This project exists to test and learn various DevOps and MLOps practices. The actual source code is trivial, but the skills learned were rather what is seen in the various testing, automation, and deployment artifacts.

## Objectives
- Understand basic use of git and Github
    - How and why to branch code and use these tools collaboratively
    - Handling merge conflicts
- Learn overall testing principles and apply unit testing using Pytest
    - Simple example using src.registration module
- Build DevOps automation using GitHub actions
    - Linting, testing, and deployment to TestPyPi
    - See deployed package using `pip install -i https://test.pypi.org/simple/ dsti-mlops-labs-egjfour`
- Build and deploy Docker containers
    - The built dockerfile is available on DockerHub at `egjfour/mlops_labs_registration`
        - After pulling from DockerHub, run **in interactive mode** with `docker run -it egjfour/mlops_labs_registration`
- Add data versioning to models and data with DVC
    - Adds the data directory and changes the wine_original dataset with versioning in DVC
    - Tests the PythonSDK in notebooks/dvc_python_sdk_explore.ipynb
- Explore data testing in Jupyter with Pytest
    - Adds notebooks/model-and-data-tests/testing_initial.ipynb
    - Shows ydata_profiling module, ipytest for testing in Jupyter and example Great Expectations usage
