import os
import pytest
from miblab import osf_upload

@pytest.mark.skipif(
    "OSF_TOKEN" not in os.environ,
    reason="OSF_TOKEN not set; skipping OSF upload test."
)
def test_osf_upload_file():
    """Test uploading a dummy text file to OSF."""
    test_filename = "test_upload.txt"
    with open(test_filename, "w") as f:
        f.write("Upload test.")

    folder = test_filename
    dataset = f"Testing/{test_filename}"
    project = "un5ct"
    token = os.getenv("OSF_TOKEN")

    # Local file must exist
    assert os.path.isfile(folder), f"Test file not found: {folder}"

    try:
        print(f"Testing osf_upload with dataset='{dataset}' to OSF project '{project}'")
        osf_upload(
            folder=folder,
            dataset=dataset,
            project=project,
            token=token,
            verbose=True,
            overwrite=True
        )
    except Exception as e:
        assert False, f"osf_upload raised an exception: {e}"
    finally:
        # Cleanup the local test file
        if os.path.exists(test_filename):
            os.remove(test_filename)

if __name__ == "__main__":
    test_osf_upload_file()