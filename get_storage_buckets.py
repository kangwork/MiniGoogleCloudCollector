import os
from fastapi import FastAPI
import uvicorn
from google.cloud import storage
from credentials import get_credentials

# 1. Create a FastAPI app
app = FastAPI()

# 2. Define the routes
# 2-1. The root route
@app.get("/")
def read_root():
    return {"message": f"미니 구글 클라우드 컬렉터 프로젝트입니다!\n'/storage/buckets'로 이동하시면 스토리지 버킷을 가져올 수 있습니다."}

# 2-2. A route to list all storage buckets in a project
@app.get("/storage/buckets")
def list_storage_buckets(project_id: str):
    credentials = get_credentials()
    storage_client = storage.Client(credentials=credentials, project=project_id)
    buckets = storage_client.list_buckets()
    bucket_names = [bucket.name for bucket in buckets]
    return {"buckets": bucket_names}

# 2-3. A route to get a storage bucket's details
@app.get("/storage/buckets/{bucket_name}")
def get_storage_bucket(project_id: str, bucket_name: str):
    credentials = get_credentials()
    storage_client = storage.Client(credentials=credentials, project=project_id)
    bucket = storage_client.get_bucket(bucket_name)
    bucket_details = {
        "name": bucket.name,
        "location": bucket.location,
        "storage_class": bucket.storage_class,
        "lifecycle_rules": bucket.lifecycle_rules,
        "labels": bucket.labels,
        "created": bucket.time_created,
    }
    return {"bucket": bucket_details}

# 3. Run the app
if __name__ == '__main__':
    # Using uvicorn, run the app
    # uvicorn is what FastAPI uses to run the app
    # We need to provide the host and port, which can be identified by running the command below in the terminal
    # gcloud compute firewall-rules list
    # (Install the Google Cloud SDK if you haven't already and init the project)
    # https://cloud.google.com/sdk/docs/install
    # The command will provide the network, priority, direction, and ports
    uvicorn.run(app, host="..." , port=...)
