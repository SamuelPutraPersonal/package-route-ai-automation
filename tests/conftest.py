# tests/conftest.py
import pytest
from src.api.package_route_api import PackageRouteAPI
import os
# Note: We import functions from test_data.images directly, not the module itself
from test_data.images import create_dummy_image, get_test_image_path
import time
from pathlib import Path # For better path handling with tmp_path

# Fixture to provide an API client instance to tests
@pytest.fixture(scope="session")
def api_client():
    """
    Provides a PackageRouteAPI client instance for tests.
    This fixture will be created once per test session.
    """
    client = PackageRouteAPI()
    yield client
    # Teardown: If we had any cleanup to do after all tests, it would go here.
    # For this in-memory SUT, there's no specific cleanup needed for the client.

@pytest.fixture(scope="function")
def clean_sut_state(api_client):
    """
    This fixture is a placeholder for cleaning the SUT state if needed.
    Since our SUT uses an in-memory DB and resets on restart,
    this fixture primarily ensures the SUT is available.
    In a real scenario, this would involve calling a cleanup endpoint
    or directly interacting with a test database.
    """
    # You might add a small delay to ensure SUT is responsive if it just started
    # time.sleep(0.5)
    # In a real app, you might have an admin endpoint to clear data
    # api_client.clear_all_data()
    yield
    # Add post-test cleanup if necessary

@pytest.fixture(scope="function")
def sample_image_path(tmp_path: Path): # Use Path for type hinting and benefits
    """
    Creates a temporary dummy image for testing and returns its path.
    Uses pytest's tmp_path fixture for a unique temporary directory.
    """
    dummy_image_filename = "test_package.jpg"
    image_file = tmp_path / dummy_image_filename
    create_dummy_image(image_file) # Create a small, valid JPEG image
    yield str(image_file) # Yield as string for os.path.basename in API client
    # tmp_path automatically cleans up the directory after the test

@pytest.fixture(scope="function")
def invalid_image_path(tmp_path: Path):
    """
    Creates a temporary invalid file for testing image upload validation.
    """
    invalid_file = tmp_path / "invalid_file.txt"
    with open(invalid_file, "w") as f:
        f.write("This is not a real image file.")
    yield str(invalid_file)

@pytest.fixture(scope="function")
def large_image_path(tmp_path: Path):
    """
    Creates a temporary large image file for performance/size testing.
    Note: This will create a ~5MB image, which might be slow.
    Adjust size or skip if not needed for your initial tests.
    """
    large_image_filename = "large_test_package.jpg"
    image_file = tmp_path / large_image_filename
    create_dummy_image(image_file, size=(2000, 2000), color=(255, 0, 0), max_bytes=5 * 1024 * 1024) # 5MB red image
    yield str(image_file)