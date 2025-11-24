"""Tests for the web application."""

import os

import pytest

from web_app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret-key"

    with app.test_client() as client:
        yield client


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary output directory and clean up after test."""
    # Save original working directory
    original_dir = os.getcwd()

    # Create temp output dir
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Change to temp directory
    os.chdir(tmp_path)

    yield output_dir

    # Restore original directory
    os.chdir(original_dir)


def test_index_page_loads(client):
    """Test that the index page loads successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"VRM Properties Scraper" in response.data
    assert b"Select States to Scrape" in response.data


def test_index_page_shows_available_states(client):
    """Test that the index page displays available states."""
    response = client.get("/")
    assert response.status_code == 200

    # Check for some expected states
    assert b"VA" in response.data
    assert b"TX" in response.data
    assert b"NC" in response.data


def test_scrape_without_states_shows_error(client):
    """Test that scraping without selecting states shows an error."""
    response = client.post("/scrape", data={}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Please select at least one state" in response.data


def test_scrape_with_invalid_state_shows_error(client):
    """Test that scraping with invalid states shows an error."""
    response = client.post("/scrape", data={"states": ["INVALID"]}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid states selected" in response.data


def test_download_invalid_file_redirects(client):
    """Test that downloading an invalid file redirects with error."""
    response = client.get("/download/malicious_file.txt", follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid file requested" in response.data


def test_download_nonexistent_file_redirects(client):
    """Test that downloading a non-existent file redirects with error."""
    response = client.get("/download/vrm_listings_2099-01-01.xlsx", follow_redirects=True)
    assert response.status_code == 200
    assert b"File not found" in response.data


def test_api_status_returns_json(client):
    """Test that the status API returns JSON."""
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.content_type == "application/json"

    data = response.get_json()
    assert "files" in data
    assert isinstance(data["files"], list)


def test_index_shows_no_files_when_empty(client, temp_output_dir):
    """Test that index shows empty state when no files are available."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"No files available yet" in response.data


def test_index_shows_files_when_available(client, temp_output_dir):
    """Test that index shows files when they exist."""
    # Create a test file
    test_file = temp_output_dir / "vrm_listings_2024-01-01.xlsx"
    test_file.write_text("test content")

    response = client.get("/")
    assert response.status_code == 200
    assert b"vrm_listings_2024-01-01.xlsx" in response.data


def test_api_status_includes_file_metadata(client, temp_output_dir):
    """Test that API status includes file metadata."""
    # Create a test file
    test_file = temp_output_dir / "vrm_listings_2024-01-01.xlsx"
    test_file.write_text("test content")

    response = client.get("/api/status")
    data = response.get_json()

    assert len(data["files"]) == 1
    assert data["files"][0]["filename"] == "vrm_listings_2024-01-01.xlsx"
    assert "size" in data["files"][0]
    assert "modified" in data["files"][0]
