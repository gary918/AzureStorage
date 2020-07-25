package com.blobs.quickstart;

/**
 * Azure VM + Managed Identity to access Azure Blob Storage
 * Enable managed identity on Azure VM: https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/qs-configure-portal-windows-vm
 * Managed Identity: https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/tutorial-linux-vm-access-storage
 * Project setup: https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-java
 * Project run:
 * - mvn compile
 * - mvn package
 * - mvn exec:java -Dexec.mainClass="com.blobs.quickstart.App" -Dexec.cleanupDaemonThreads=false
 */
import com.azure.storage.blob.*;
import com.azure.storage.blob.models.*;
import com.azure.identity.*;

import java.io.*;

public class App
{
    public static void main( String[] args ) throws IOException
    {
        System.out.println("Azure Blob Storage ...");

        //String connectStr ="storageconnectstring";
        String endpoint = "https://<storageAccount>.blob.core.windows.net";

        // Create a BlobServiceClient object which will be used to create a container client
        //BlobServiceClient blobServiceClient = new BlobServiceClientBuilder().connectionString(connectStr).buildClient();
        BlobServiceClient blobServiceClient = new BlobServiceClientBuilder()
        .endpoint(endpoint)
        .credential(new ManagedIdentityCredentialBuilder().build()) // Or use DefaultAzureCredentialBuilder
        .buildClient();

        //Create a unique name for the container
        String containerName = "<containerName>";
        //BlobContainerClient containerClient = blobServiceClient.createBlobContainer(containerName);
        BlobContainerClient containerClient = blobServiceClient.getBlobContainerClient(containerName);

        System.out.println("\nListing blobs...");
        // List the blob(s) in the container.
        for (BlobItem blobItem : containerClient.listBlobs()) {
            System.out.println("\t" + blobItem.getName());
        }
    }
}
