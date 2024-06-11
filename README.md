# MiniGoogleCloudCollector
A repository for the SpaceONE Mini Google Collector Assignment

This program retrieves data from Google Cloud Platform (GCP) and displays it in a web browser.


The program retrieves the following data from GCP:
- Storage buckets
- IAM roles
- VM instances


Note that the GOOGLE_APPLICATION_CREDENTIALS environment variable must be set to the path of the credentials file. 

## How to Set Up the Environment Variable
Follow the instructions below to set up the GOOGLE_APPLICATION_CREDENTIALS environment variable.
1. Open a terminal.
2. Run the following command:
   ```shell
   export GOOGLE_APPLICATION_CREDENTIALS="../local/mini-collector/key.json"
   ```
3. Replace "../local/mini-collector/key.json" with the path to your credentials file.


## How to Run the Program
1. Navigate to `src/`.

2. Execute the main program.
    (Note: Make sure you installed all the dependencies in your environment.)

    You can execute the program by simply running:
    ```shell
    make run
    ```

    Or, run the following command to start the program manually.
    ```shell
    uvicorn main:app --reload
    ```

3. Open a web browser and go to http://localhost:8000 to view the data.

4. Press Ctrl+C to stop the program.


## Modules
The program uses the following modules:
- resources/storage_buckets.py
- resources/iam_roles.py
- resources/vm_instances.py
- utils/credentials.py
- utils/logging.py
- utils/resource.py
- utils/roles.py
- utils/vm_instances.py
- main.py
