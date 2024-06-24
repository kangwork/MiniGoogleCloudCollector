# MiniGoogleCloudCollector
This program retrieves data from Google Cloud Platform (GCP) and displays it in a web browser.

The program retrieves the following data from GCP:
- Storage buckets
- IAM roles
- VM instances

## How to Run the Program

There are two simple ways to run the program:

[A. Using Docker](#a-using-docker) (No cloning required <span style="color: grey"> unless you want to encrypt your credentials key file.</span>)

[B. Using Python](#b-using-python) (You will need to install Python and its dependencies.)

We recommend using Docker to run the program.

### A. Using Docker

To run the program using Docker, follow these steps:

1. <u>**Pull the Docker image from Docker Hub.**</u>

    You can find the latest version of the Docker image at this link: [Docker Hub](https://hub.docker.com/r/irenekang/minigooglecloudcollector/tags?page=1&ordering=last_updated)

    Pull the Docker image by running the following command:
    ```bash
    docker pull irenekang/minigooglecloudcollector:v1.0.1
    ```
2. <u>**Run the Docker container.**</u>

    There are four options when running the Docker container. You can choose one of the following options:
    <!-- <!-- list of links to headings -- To use link to headings, use the following format: [link text](#heading-name) -->
    [1) Basic run](#1-basic-run)

    [2) Run with logs](#2-run-with-logs)

    [3) Run with credentials key file](#3-run-with-credentials-key-file)

    [4) Run with logs and credentials key file](#4-run-with-logs-and-credentials-key-file)


    #### 1) Basic run
    ```bash
    docker run -p 8000:8000 irenekang/minigooglecloudcollector:v1.0.1
    ```

    <br><br>

    #### 2) Run with logs
    Make sure you have a directory that you can mount to the container.
    You will be able to retrieve the `log.log` file in the directory you mounted.
    ```bash
    docker run -p 8000:8000 -v $(pwd)/mnt/logs:/mnt/logs irenekang/minigooglecloudcollector:v1.0.1
    ```
    Replace `$(pwd)/mnt/logs` with the path to the directory where you want to save the log file.

    <br><br>

    #### 3) Run with credentials key file

    **3-1) Encrypt your key file.**
    
    For the security of your GCP account, we ask you to encrypt your credentials key file before mounting it to the container.

    To do that, we have written a script for you: [encrypt_key_file.sh](encrypt_key_file.sh).

    You can also download the script by running the following command:

    ```bash
    curl -O https://raw.githubusercontent.com/kangwork/MiniGoogleCloudCollector/main/encrypt_key_file.sh
    ```
    
    Then, run the script by running the following command:

    ```bash
    ./encrypt_key_file.sh
    ```

    You will be asked to enter your credentials key file path and set your own *password*.

    Then, as the message says, the encrypted file will be saved in `mnt/encrypted_keys` directory.

    You can rename the directory(not the file itself), but you will need to mount the directory to the container's `/mnt/encrypted_keys` directory.

    <br>

    **3-2) Mount the encrypted key file to the container.**

    You have to pass the *password* as ENCRYPTION_KEY you entered when encrypting the key file as an environment variable.

    ```bash
    docker run -p 8000:8000 -v $(pwd)/mnt/encrypted_keys:/mnt/encrypted_keys -e ENCRYPTION_KEY=password irenekang/minigooglecloudcollector:v1.0.1
    ```

    You can replace `$(pwd)/mnt/encrypted_keys` with the path to the directory where the encrypted key file(`key.json.gpg`) is located.
    Replace `password` with the password you set when encrypting the key file.

    <br><br>


    #### 4) Run with logs and credentials key file
    
    Follow the steps in [3) Run with credentials key file](#3-run-with-credentials-key-file) to encrypt your key file and mount it to the container.

    You can run the container with logs and credentials key file by running the following command:

    ```bash
    docker run -p 8000:8000 -v /path/to/your/logs/directory:/mnt/logs -v /path/to/your/encrypted_keys/directory:/mnt/encrypted_keys -e ENCRYPTION_KEY=password irenekang/minigooglecloudcollector:v1.0.1
    ```

<br><br><br>

### B. Using Python

To run the program by cloning the repository, follow these steps:

1. <u>**Clone the repository**</u>
    
    <br><br>

2. <u>**Navigate to the `src` directory**</u>

    <br><br>

3. <u>*(Optional)* **Assuming you have Python installed, create a virtual environment and activate it**</u>
    ```bash
    make activate
    ```
    (If you don't have Python installed, you can install it by following the instructions at this link: [Python Installation Guide](https://realpython.com/installing-python/))

    Follow the message in the terminal to activate the virtual environment.

    <br><br>

4. <u>*(Optional)* **To use the credentials key file:**</u>
    
    **4-1) Encrypt your key file.**
    ```bash
    ../encrypt_key_file.sh
    ```

    **4-2) Set your *password* as an environment variable.**
    ```bash
    export ENCRYPTION_KEY=password
    ```
    Replace `password` with the password you set when encrypting the key file.

<br><br>

5. <u>**Run the program**</u>
- If you have set up a virtual environment, run the following command:
    ```bash
    make run
    ```
- Otherwise, run the following command:
    ```bash
    pip install -r ../pkg/pip_requirements.txt
    python main.py
    ```

