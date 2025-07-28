# src/api/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ApiConfig:
    # Base URL for the System Under Test (SUT) API
    BASE_URL = os.getenv("PRIME_VISION_SUT_API_BASE_URL", "http://127.0.0.1:5000")

    # API Endpoints
    INGEST_PACKAGE_ENDPOINT = f"{BASE_URL}/packages/ingest"
    GET_PACKAGE_STATUS_ENDPOINT = f"{BASE_URL}/packages" # /<package_id>/status
    GET_SUMMARY_REPORT_ENDPOINT = f"{BASE_URL}/reports/summary"