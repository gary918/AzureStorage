# Need to install the following libs to get started:
# pip install azure.storage.blob
# pip install aiohttp

import asyncio
import json
import logging
import os
import sys
import time
from azure.storage.blob.aio import BlobServiceClient
from azure.storage.blob.aio import ContainerClient
from azure.storage.blob.aio import BlobClient
from dotenv import load_dotenv
from opencensus.ext.azure.log_exporter import AzureLogHandler


# Init
def init():
    # Load environment variables
    load_dotenv()
    # Init the logger
    logger = logging.getLogger(os.getenv("LOG_NAME"))
    logger.setLevel(logging.DEBUG)
    # Create file handler to store the log
    fh = logging.FileHandler(os.path.join(os.getenv("LOCAL_DIR"),os.getenv("LOG_NAME")+".log"))
    fh.setLevel(logging.DEBUG)
    # Create console handler to show the log on the screen
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)
    # Create Azure Application Insights handler
    ah = AzureLogHandler()
    ah.setLevel(logging.DEBUG)
    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    ah.setFormatter(formatter)
    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.addHandler(ah)

# Get the file path from the blob_name
def get_file_path(blob_name):   
    local_dir = os.getenv("LOCAL_DIR")
    file_path = os.path.join(local_dir,blob_name)
    file_exists = False
    # Check if the os is Windows
    if os.name=="nt":
        file_path = file_path.replace("/","\\")
    if os.path.exists(file_path):
        print("File exists: %s" % file_path)
        file_exists = True
    else:
        dir_name = os.path.dirname(file_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    return file_exists,file_path


# Download the file specified in the file_path
async def downloadBlob(blob_client, file_path):
    async with blob_client as blob:
        with open(file_path, "wb") as my_blob:
            try:
                stream = await blob.download_blob()
                data = await stream.readall()
                my_blob.write(data)
                logger = logging.getLogger(os.getenv("LOG_NAME"))
                logger.info("Success: %s" % file_path)
            except Exception as error:
                error_message = 'Failed: '+ file_path + 'Error message: ' + str(error)
                logger.info(error_message)


# Download the files in the path
async def downloadPath(container_client,path):
    tasks=[]
    
    async with container_client:
        async for blob in container_client.walk_blobs(name_starts_with=path,delimiter='/'):
            # Filter out the directories
            if blob.name.endswith("/"):
                continue
            print(blob.name)

            file_exists, file_path=get_file_path(blob.name)
            if file_exists:
                return
            blob_client = container_client.get_blob_client(blob)
            tasks.append(downloadBlob(blob_client, file_path))
        
        if tasks:    
            await asyncio.wait(tasks)


# Download all files in the list of path
def download(paths):
    now = lambda: time.time()
    start = now()

    tasks=[]
    for path in paths:
        container_client = ContainerClient.from_connection_string(
            conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING"),
            container_name=os.getenv("CONTAINER_NAME"))
        tasks.append(downloadPath(container_client,path))

    if tasks:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        
    print('TIME: ', now() - start)


# Should read from .json file
# Need to download the files in the folder in the list of paths_to_download
def get_paths_to_download():
    # Read the paths in the CONTAINER_NAME in Azure Blob Storage 
    paths_to_download = ["example/data/",
                         "example/data/xxx/",
                         "example/xxx/",
                         "HSamples/xxx/Food/",
                         "HSamples/xxx/Drinks/"]
    return paths_to_download


# Read json file to get the paths to download files from Azure Blob Storage
# Need to download the files in the folder in the list of paths_to_download
def read_paths_to_download():
    paths =[]
    with open(os.getenv("CONFIG_FILE")) as json_file:
        records=json.load(json_file)
        for record in records:
            print(record["entity_uuid"])
            for metadata in record["metadata"]:
                if metadata["attribute"]=="location":
                    print(metadata["value"])
                    paths.append(metadata["value"])
    return paths


def main():
    init()
    paths_to_download = read_paths_to_download()
    download(paths_to_download)


if __name__=="__main__":
    main()