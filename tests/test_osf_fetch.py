import os
import shutil
from miblab.data import osf_fetch

def test_osf_fetch():
    # Set test parameters
    folder = "test_download"
    dataset = "TRISTAN/RAT/bosentan_highdose/Sanofi"  # If empty, will download everything
    project_id = "un5ct"  # Public project for default test

    # Optional: Token for private project test
    token = os.getenv('OSF_TOKEN')  # Read token from environment variable if available

    # Clean up before running
    if os.path.exists(folder):
        shutil.rmtree(folder)

    # Run osf_fetch
    try:
        print(f"Testing osf_fetch with dataset '{dataset}' (token={'provided' if token else 'not provided'})...")
        osf_fetch(folder=folder, dataset=dataset, project_id=project_id, token=token, extract=True, verbose=True)
    except Exception as e:
        print(f"Test failed with error: {e}")
        return

    # Check that something got downloaded
    if not os.path.exists(folder):
        print("Test failed: folder not created.")
    elif not any(os.scandir(folder)):
        print("Test failed: no files downloaded.")
    else:
        print("Test passed: files downloaded successfully.")

    # Clean up after test (optional: comment out if you want to inspect)
    # shutil.rmtree(folder)
    print(f"Test folder left at: {folder}")

if __name__ == "__main__":
    test_osf_fetch()