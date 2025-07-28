# tests/api/test_package_ingestion.py
import pytest
import allure
import os
import requests
from src.api.config import ApiConfig
from requests.exceptions import HTTPError

@allure.feature("Package Ingestion")
@allure.story("Ingest New Package")
class TestPackageIngestion:

    @allure.title("Verify successful package ingestion and routing")
    @allure.description(
        "This test verifies that a new package can be successfully ingested "
        "via the API, and its status changes to 'ROUTED' with valid recognition "
        "data and a routing decision."
    )
    @allure.tag("HappyPath", "API", "Ingestion", "Routing")
    # We use sample_image_path fixture, so no need for parametrize for different image names here
    def test_successful_ingestion(self, api_client, sample_image_path):
        with allure.step(f"Ingest package with image: {os.path.basename(sample_image_path)}"):
            # Use the dynamically created sample_image_path
            response = api_client.ingest_package(sample_image_path)
            allure.attach(str(response), name="API Response", attachment_type=allure.attachment_type.JSON)

        with allure.step("Verify response status and content"):
            assert response['message'] == "Package ingested and processed"
            assert 'package_id' in response
            assert response['status'] == "ROUTED"
            assert 'recognition_data' in response
            assert 'route_decision' in response
            assert response['recognition_data']['package_type'] is not None
            assert response['recognition_data']['destination_address'] is not None
            assert response['route_decision'] is not None

        package_id = response['package_id']
        with allure.step(f"Retrieve package status for ID: {package_id}"):
            status_response = api_client.get_package_status(package_id)
            allure.attach(str(status_response), name="Status API Response", attachment_type=allure.attachment_type.JSON)

        with allure.step("Verify retrieved status is 'ROUTED'"):
            assert status_response['package_id'] == package_id
            assert status_response['status'] == "ROUTED"
            assert status_response['route_decision'] == response['route_decision'] # Should match initial decision

    @allure.title("Verify package ingestion with invalid image format")
    @allure.description(
        "This test attempts to ingest a package with a non-image file "
        "and verifies that the API returns a 400 Bad Request error."
    )
    @allure.tag("NegativeTest", "API", "Validation")
    def test_ingest_invalid_image_format(self, api_client, invalid_image_path):
        with allure.step(f"Attempt to ingest invalid file: {os.path.basename(invalid_image_path)}"):
            # When using requests, 4xx/5xx responses raise HTTPError if response.raise_for_status() is called
            with pytest.raises(HTTPError) as excinfo:
                api_client.ingest_package(invalid_image_path)

            assert excinfo.value.response.status_code == 400
            error_response = excinfo.value.response.json()
            allure.attach(str(error_response), name="Error API Response", attachment_type=allure.attachment_type.JSON)
            assert "error" in error_response
            assert "Invalid image file format or corrupted" in error_response["error"]

    @allure.title("Verify ingestion with no image file provided")
    @allure.description(
        "This test verifies the API handles requests with no image file "
        "attached, returning a 400 Bad Request error."
    )
    @allure.tag("NegativeTest", "API", "Validation")
    def test_ingest_no_image_file(self, api_client):
        with allure.step("Attempt to ingest without providing an image file"):
            # Manually construct a requests call to simulate missing file part
            url = ApiConfig.INGEST_PACKAGE_ENDPOINT # Use direct endpoint from config
            with pytest.raises(HTTPError) as excinfo:
                # Send a POST request with an empty 'files' dictionary
                requests.post(url, files={}).raise_for_status()

            assert excinfo.value.response.status_code == 400
            error_response = excinfo.value.response.json()
            allure.attach(str(error_response), name="Error API Response", attachment_type=allure.attachment_type.JSON)
            assert "error" in error_response
            assert "No image file provided" in error_response["error"]

@allure.feature("Package Status and Reports")
@allure.story("Retrieve Status and Summary")
class TestPackageStatusAndReports:

    @allure.title("Verify retrieving status of a non-existent package")
    @allure.description(
        "This test verifies that querying the status of a package_id "
        "that does not exist returns a 404 Not Found error."
    )
    @allure.tag("NegativeTest", "API", "Status")
    def test_get_non_existent_package_status(self, api_client):
        non_existent_id = "non-existent-package-id-123"
        with allure.step(f"Attempt to get status for non-existent ID: {non_existent_id}"):
            with pytest.raises(HTTPError) as excinfo:
                api_client.get_package_status(non_existent_id)

            assert excinfo.value.response.status_code == 404
            error_response = excinfo.value.response.json()
            allure.attach(str(error_response), name="Error API Response", attachment_type=allure.attachment_type.JSON)
            assert "error" in error_response
            assert "Package not found" in error_response["error"]

    @allure.title("Verify summary report is retrievable")
    @allure.description(
        "This test ensures that the summary report endpoint is accessible "
        "and returns a valid JSON structure."
    )
    @allure.tag("HappyPath", "API", "Report")
    def test_get_summary_report(self, api_client):
        with allure.step("Retrieve summary report"):
            response = api_client.get_summary_report()
            allure.attach(str(response), name="API Response", attachment_type=allure.attachment_type.JSON)

        with allure.step("Verify report structure"):
            assert "total_packages_processed" in response
            assert "total_packages_routed" in response
            assert "total_errors" in response
            assert "route_distribution" in response
            assert isinstance(response["total_packages_processed"], int)
            assert isinstance(response["total_packages_routed"], int)
            assert isinstance(response["total_errors"], int)
            assert isinstance(response["route_distribution"], dict)