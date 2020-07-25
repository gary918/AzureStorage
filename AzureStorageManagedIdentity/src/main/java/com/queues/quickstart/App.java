package com.queues.quickstart;
 
/**
 * Azure VM + Managed Identity to access Azure Queue Storage
 * Enable managed identity on Azure VM: https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/qs-configure-portal-windows-vm
 * Managed Identity: https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/tutorial-linux-vm-access-storage
 * - Goto Storage Account -> Access control -> Add a role assignment
 *  o Add Storage Queue Data Contributor
 *  o Add Storage Queue Data Message Processor
 *  o Add Storage Queue Data Message Reader
 *  o Add Storage Queue Data Reader
 * Project setup: https://docs.microsoft.com/en-us/azure/storage/queues/storage-quickstart-queues-java
 * Project run:
 * - mvn compile
 * - mvn package
 * - mvn exec:java -Dexec.mainClass="com.queues.quickstart.App" -Dexec.cleanupDaemonThreads=false
 */
import com.azure.storage.queue.*;
import com.azure.storage.queue.models.*;
import com.azure.identity.*;

import java.io.*;
import java.time.*;

 public class App 
{
    public static void main( String[] args )
    {
        String queueName = "quickstartqueues-" + java.util.UUID.randomUUID();
        String queueServiceURL = "https://<storageAccount>.queue.core.windows.net";
        
        System.out.println("Creating queue: " + queueName);

        // Instantiate a QueueClient which will be
        // used to create and manipulate the queue
        QueueServiceClient queueServiceClient = new QueueServiceClientBuilder()
        .endpoint(queueServiceURL)
        .credential(new ManagedIdentityCredentialBuilder().build()) // Or use DefaultAzureCredentialBuilder
        .buildClient();

        // Create the queue
        QueueClient queueClient = queueServiceClient.createQueue(queueName);


        System.out.println("\nAdding messages to the queue...");

        // Send several messages to the queue
        queueClient.sendMessage("First message");
        queueClient.sendMessage("Second message");

        // Save the result so we can update this message later
        SendMessageResult result = queueClient.sendMessage("Third message");

        System.out.println("\nPeek at the messages in the queue...");

        // Peek at messages in the queue
        queueClient.peekMessages(10, null, null).forEach(
            peekedMessage -> System.out.println("Message: " + peekedMessage.getMessageText()));

        System.out.println("\nPress Enter key to delete the queue...");
        System.console().readLine();
        
        // Clean up
        System.out.println("Deleting queue: " + queueClient.getQueueName());
        queueClient.delete();
        
        System.out.println("Done");
        
    }
}
