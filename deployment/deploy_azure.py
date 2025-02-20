import os
from azure.storage.blob import BlobServiceClient
from utilities.logger import Logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve Azure Storage credentials from environment variables
AZURE_STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT")
AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")

class AzureDeployer:
    """Handles deployment of trading bot files to Azure Blob Storage."""

    def __init__(self):
        """Initialize Azure Blob Service Client."""
        if not AZURE_STORAGE_ACCOUNT or not AZURE_STORAGE_KEY or not AZURE_CONTAINER_NAME:
            Logger.log_error("❌ Azure Storage credentials are missing. Check your environment variables.")
            raise ValueError("Azure credentials not found.")
        
        self.blob_service_client = BlobServiceClient(
            account_url=f"https://{AZURE_STORAGE_ACCOUNT}.blob.core.windows.net",
            credential=AZURE_STORAGE_KEY
        )
        self.container_client = self.blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
        
        # Ensure container exists
        self.ensure_container_exists()

    def ensure_container_exists(self):
        """Create container if it doesn't exist."""
        try:
            self.container_client.get_container_properties()
            Logger.log_system(f"📦 Container '{AZURE_CONTAINER_NAME}' exists.")
        except Exception:
            self.container_client.create_container()
            Logger.log_system(f"✅ Created new container: {AZURE_CONTAINER_NAME}")

    def upload_file(self, local_path, remote_filename):
        """Upload a file to Azure Blob Storage."""
        try:
            blob_client = self.container_client.get_blob_client(remote_filename)
            
            with open(local_path, "rb") as file_data:
                blob_client.upload_blob(file_data, overwrite=True)
            
            Logger.log_system(f"📤 Uploaded {local_path} → {remote_filename} in Azure Storage.")
        except Exception as e:
            Logger.log_error(f"❌ Error uploading {local_path} to Azure: {e}")

    def deploy_directory(self, local_directory, azure_prefix=""):
        """Upload all files from a local directory to Azure Storage."""
        if not os.path.exists(local_directory):
            Logger.log_error(f"❌ Directory not found: {local_directory}")
            return
        
        for root, _, files in os.walk(local_directory):
            for file in files:
                local_path = os.path.join(root, file)
                remote_filename = os.path.join(azure_prefix, os.path.relpath(local_path, local_directory)).replace("\\", "/")
                self.upload_file(local_path, remote_filename)

        Logger.log_system(f"🚀 Successfully deployed {local_directory} to Azure.")

# If running this script independently, trigger deployment
if __name__ == "__main__":
    try:
        deployer = AzureDeployer()
        deployer.deploy_directory("bot_files")  # Adjust this path to your bot’s directory
    except Exception as e:
        Logger.log_error(f"❌ Deployment failed: {e}")
