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
    return {"message": "Welcome to the Google Cloud Resource Collector"}

# 2-2. A route to list all storage buckets in a project
@app.get("/storage/buckets")
def list_storage_buckets(project_id: str):
    credentials = get_credentials()
    storage_client = storage.Client(credentials=credentials, project=project_id)
    buckets = storage_client.list_buckets()
    bucket_names = [bucket.name for bucket in buckets]
    return {"buckets": bucket_names}

# 3. Run the app
if __name__ == '__main__':
    uvicorn.run(app, host="
