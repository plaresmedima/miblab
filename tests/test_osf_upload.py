import os
import pytest
import requests
from miblab import osf_upload

PROJECT = "un5ct"
PING_URL = f"https://api.osf.io/v2/nodes/{PROJECT}"

# Check if OSF is reachable (200) – otherwise skip the test
try:
    OSF_UP = requests.head(PING_URL, timeout=5).status_code == 200
except requests.exceptions.RequestException:
    OSF_UP = False

# Test definition
@pytest.mark.skipif("OSF_TOKEN" not in os.environ,
                    reason="OSF_TOKEN not set; skipping OSF upload test.")
@pytest.mark.skipif(not OSF_UP,
                    reason="OSF unreachable or returned non-200; skipping upload test.")

def test_osf_upload_file():
    # Create a small dummy file
    test_filename = "test_upload.txt"
    with open(test_filename, "w") as f:
        f.write("Upload test.")

    folder = test_filename                     # local file path
    dataset = f"Testing/{test_filename}"       # remote OSF path
    token = os.getenv("OSF_TOKEN")

    try:
        # Run the upload
        osf_upload(
            folder=folder,
            dataset=dataset,
            project=PROJECT,
            token=token,
            verbose=True,
            overwrite=True
        )
    except Exception as e:
        assert False, f"osf_upload raised an exception: {e}"
    finally:
        # Remove local dummy file
        if os.path.exists(test_filename):
            os.remove(test_filename)

if __name__ == "__main__":
    test_osf_upload_file()