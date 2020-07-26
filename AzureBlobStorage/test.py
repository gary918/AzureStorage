import os
import sys
import asyncio
from azure.storage.blob.aio import ContainerClient

async def main():
    try:
        CONNECTION_STRING = "xxxx"
    except KeyError:
        print("AZURE_STORAGE_CONNECTION_STRING must be set.")
        sys.exit(1)

    container = ContainerClient.from_connection_string(CONNECTION_STRING, container_name="containerName")
    path="example/data/"
    async with container:
        async for blob in container.list_blobs(name_starts_with=path):
            print(blob.name + '\n')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())