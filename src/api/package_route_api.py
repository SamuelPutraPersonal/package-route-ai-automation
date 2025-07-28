# src/api/package_route_api.py
import requests
from src.api.config import ApiConfig
import logging
import os # Added for os.path.basename

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PackageRouteAPI:
    def __init__(self, base_url=ApiConfig.BASE_URL):
        self.base_url = base_url
        logger.info(f"API Client initialized with base URL: {self.base_url}")
        self.session = requests.Session() # Use a session for persistent connections

    def ingest_package(self, image_path):
        """
        Sends a POST request to ingest a package with an image.
        """
        url = ApiConfig.INGEST_PACKAGE_ENDPOINT
        logger.info(f"Sending POST request to {url} with image: {image_path}")
        try:
            # 'rb' means read in binary mode
            with open(image_path, 'rb') as f:
                files = {'image': (os.path.basename(image_path), f, 'image/jpeg')}
                response = self.session.post(url, files=files)
                response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
                logger.info(f"Ingest response status: {response.status_code}")
                return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error ingesting package from {image_path}: {e}")
            raise
        except FileNotFoundError:
            logger.error(f"Image file not found: {image_path}")
            raise

    def get_package_status(self, package_id):
        """
        Sends a GET request to retrieve the status of a specific package.
        """
        url = f"{ApiConfig.GET_PACKAGE_STATUS_ENDPOINT}/{package_id}/status"
        logger.info(f"Sending GET request to {url}")
        try:
            response = self.session.get(url)
            response.raise_for_status()
            logger.info(f"Status response status: {response.status_code}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting status for package ID {package_id}: {e}")
            raise

    def get_summary_report(self):
        """
        Sends a GET request to retrieve the summary report.
        """
        url = ApiConfig.GET_SUMMARY_REPORT_ENDPOINT
        logger.info(f"Sending GET request to {url}")
        try:
            response = self.session.get(url)
            response.raise_for_status()
            logger.info(f"Summary report status: {response.status_code}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting summary report: {e}")
            raise