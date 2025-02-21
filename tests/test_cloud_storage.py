import unittest
import json
import os
from utilities.cloud_storage import CloudStorage

class TestCloudStorage(unittest.TestCase):
    """ Unit tests for AI-powered cloud data management """

    @classmethod
    def setUpClass(cls):
        """ Load config and initialize CloudStorage """
        with open("config/config.json", "r") as f:
            cls.config = json.load(f)

        cls.cloud_storage = CloudStorage(cls.config)

    def test_upload_file(self):
        """ Ensure AI correctly uploads files to the cloud """
        test_file_path = "logs/test_log.txt"
        test_content = "AI Cloud Storage Test"

        # Create test file
        with open(test_file_path, "w") as f:
            f.write(test_content)

        upload_result = self.cloud_storage.upload_file(test_file_path, "test_folder/test_log.txt")

        self.assertTrue(upload_result, "File should be successfully uploaded")

        # Clean up local file
        os.remove(test_file_path)

    def test_download_file(self):
        """ Ensure AI correctly retrieves files from the cloud """
        cloud_path = "test_folder/test_log.txt"
        local_path = "logs/downloaded_test_log.txt"

        download_result = self.cloud_storage.download_file(cloud_path, local_path)

        self.assertTrue(download_result, "File should be successfully downloaded")
        self.assertTrue(os.path.exists(local_path), "Downloaded file should exist locally")

        # Clean up downloaded file
        os.remove(local_path)

    def test_list_cloud_files(self):
        """ Validate AI retrieves a list of stored cloud files """
        file_list = self.cloud_storage.list_files("test_folder/")

        self.assertIsInstance(file_list, list, "File list should be a list")
        self.assertGreaterEqual(len(file_list), 1, "Cloud storage should contain at least one file")

    def test_delete_cloud_file(self):
        """ Ensure AI correctly deletes files from the cloud """
        cloud_path = "test_folder/test_log.txt"
        delete_result = self.cloud_storage.delete_file(cloud_path)

        self.assertTrue(delete_result, "File should be successfully deleted")

    def test_cloud_storage_error_handling(self):
        """ Validate AI handles cloud storage failures gracefully """
        invalid_path = "non_existent_folder/missing_file.txt"
        download_result = self.cloud_storage.download_file(invalid_path, "logs/fail_test.txt")

        self.assertFalse(download_result, "AI should return False for missing cloud files")

if __name__ == "__main__":
    unittest.main()
