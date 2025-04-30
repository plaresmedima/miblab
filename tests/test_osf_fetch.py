import os
import shutil
from miblab import osf_fetch  # Updated import path per review

def test_osf_fetch():
    # Set test parameters
    dataset = "TRISTAN/RAT/bosentan_highdose/Sanofi"  # Example dataset
    folder = "test_download"
    project_id = "un5ct"  # Public OSF project
    token = os.getenv('OSF_TOKEN')  # Optional: for private projects

    # Clean up before test
    if os.path.exists(folder):
        shutil.rmtree(folder)

    # Run osf_fetch
    try:
        print(f"Testing osf_fetch with dataset='{dataset}' and token={'provided' if token else 'not provided'}")
        osf_fetch(dataset=dataset, folder=folder, project_id=project_id, token=token, extract=True, verbose=True)
    except Exception as e:
        assert False, f"osf_fetch raised an exception: {e}"

    # Assertions (pytest-compatible)
    assert os.path.exists(folder), "Folder was not created"
    assert any(os.scandir(folder)), "No files were downloaded"

    # Leave folder for inspection (optional)
    print(f"Test passed. Downloaded files are in: {folder}")
    # To auto-cleanup after the test, uncomment below:
    # shutil.rmtree(folder)

if __name__ == "__main__":
    test_osf_fetch()