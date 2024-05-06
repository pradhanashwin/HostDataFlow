Data Pipeline for Host Fetching, Normalization, and Deduping
This repository contains a Python script for implementing a data pipeline that fetches raw hosts from third-party vendors, normalizes the hosts into a unified format, and dedupes the hosts. The script uses Python 3.10 and MongoDB for data storage.

## Project structure
```bash
HostDataFlow
├── README.md
├── __init__.py
├── clients.py
├── config.py
├── data_deduping.py
├── example.env
├── normalization.py
├── pipeline.py
├── plot.py
└── requirements.txt
```

This application can be configured with environment variables.

You can create `.env` file in the root directory or rename
`example.env` to `.env` and place all
environment variables here

## Installation

### Using virtual environment
**Create a virtual environment and install dependencies using Conda**

1. Create a New Conda Environment:

    Open your terminal or command prompt and use the following command to create a new Conda environment. Replace `myenv` with the name you'd like to give to your environment.

    ```shell
    conda create --name pipeline python=3.10
    ```

   This command will create a new Conda environment named `pipeline` and use Python 3.10.

2. Activate the Conda Environment**:

    Once the environment is created, activate it using the following command:

    ```shell
    conda activate pipeline
    ```

    Replace `pipeline` with the name of your Conda environment.

    After you activated the enviroment install the dependencies.

    ```bash
    pip install -r requirements.txt
    ```

3. Make sure you have installed mongodb

    [Follow Installation Here](https://www.mongodb.com/docs/manual/installation/https://www.mongodb.com/docs/manual/installation/).


## Running the application

After installation is completed you can run the project using 

    ```bash
     python pipeline.py --limit=2 --skip=2  
    ```

    here limit and skip is an optional value which will be set to 1 by default