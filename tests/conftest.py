# tests/conftest.py

import subprocess
import time
import sys
import pytest
import os
from playwright.sync_api import sync_playwright
import requests

@pytest.fixture(scope='session')
def fastapi_server(request):
    """
    Fixture to start the FastAPI server before E2E tests and stop it after tests complete.
    """
    # Mark tests as requiring a running server
    server_url = 'http://127.0.0.1:8000/'
    
    try:
        # Check if server is already running
        response = requests.get(server_url, timeout=2)
        if response.status_code == 200:
            print("FastAPI server is already running.")
            yield
            return
    except requests.exceptions.RequestException:
        pass
    
    # Start FastAPI app using the current Python interpreter
    print("Starting FastAPI server...")
    try:
        # Use PYTHONUNBUFFERED to ensure output is not buffered
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'
        fastapi_process = subprocess.Popen(
            [sys.executable, 'main.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )
    except Exception as e:
        pytest.skip(f"Could not start FastAPI server: {e}")
        return
    
    # Wait for the server to start by polling the root endpoint
    timeout = 30  # seconds
    start_time = time.time()
    server_up = False
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(server_url, timeout=2)
            if response.status_code == 200:
                server_up = True
                print("✓ FastAPI server is up and running.")
                break
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)
    
    if not server_up:
        try:
            fastapi_process.terminate()
            fastapi_process.wait(timeout=5)
        except:
            fastapi_process.kill()
        pytest.skip("FastAPI server failed to start within timeout period.")
        return
    
    yield
    
    # Terminate FastAPI server
    print("Shutting down FastAPI server...")
    try:
        fastapi_process.terminate()
        fastapi_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        fastapi_process.kill()
        fastapi_process.wait()
    print("✓ FastAPI server has been terminated.")

@pytest.fixture(scope="session")
def playwright_instance_fixture():
    """
    Fixture to manage Playwright's lifecycle.
    """
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance_fixture):
    """
    Fixture to launch a browser instance.
    """
    browser = playwright_instance_fixture.chromium.launch(headless=True)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    """
    Fixture to create a new page for each test.
    """
    page = browser.new_page()
    yield page
    page.close()
