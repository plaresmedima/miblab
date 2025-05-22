import os
from miblab import osf_upload

def test_osf_upload_file():
    """Test uploading a dummy text file to OSF."""
    test_filename = "test_upload.txt"
    with open(test_filename, "w") as f:
        f.write("Upload test.")

    token = os.getenv("OSF_TOKEN")
    assert token, "OSF token not provided. Set OSF_TOKEN in the environment."

    project = "un5ct"
    dataset = f"Testing/{test_filename}"

    try:
        osf_upload(
            folder=test_filename,
            dataset=dataset,
            project=project,
            token=token,
            verbose=False,
            overwrite=True
        )
    finally:
        os.remove(test_filename)