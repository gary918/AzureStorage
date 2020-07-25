# Azure VM + Managed Identity Access Azure Storage

## Azure VM + Managed Identity to access Azure Blob Storage
 * Enable managed identity on Azure VM: https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/qs-configure-portal-windows-vm
 * Managed Identity: https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/tutorial-linux-vm-access-storage
 * Project setup: https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-java
 * Project run:
    * mvn compile
    * mvn package
    * mvn exec:java -Dexec.mainClass="com.blobs.quickstart.App" -Dexec.cleanupDaemonThreads=false
## Azure VM + Managed Identity to access Azure Queue Storage
 * Enable managed identity on Azure VM: https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/qs-configure-portal-windows-vm
 * Managed Identity: https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/tutorial-linux-vm-access-storage
    * Goto Storage Account -> Access control -> Add a role assignment
        * Add Storage Queue Data Contributor
        * Add Storage Queue Data Message Processor
        * Add Storage Queue Data Message Reader
        * Add Storage Queue Data Reader
 * Project setup: https://docs.microsoft.com/en-us/azure/storage/queues/storage-quickstart-queues-java
 * Project run:
    * mvn compile
    * mvn package
    * mvn exec:java -Dexec.mainClass="com.queues.quickstart.App" -Dexec.cleanupDaemonThreads=false