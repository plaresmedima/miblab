import os
import shutil
from miblab import osf_upload

def test_osf_upload_file():
    """Test uploading a dummy text file to OSF."""
    test_filename = "test_upload.txt"
    with open(test_filename, "w") as f:
        f.write("Upload test.")

    folder = test_filename
    dataset = f"Testing/{test_filename}"
    project = "un5ct"
    token = os.getenv("OSF_TOKEN")

    assert os.path.isfile(folder), f"Test file not found: {folder}"
    assert token, "OSF token not provided. Set OSF_TOKEN in the environment."

    # Run osf_upload
    try:
        print(f"Testing osf_upload with dataset='{dataset}' to OSF project '{project}'")
        osf_upload(folder=folder, dataset=dataset, project=project, token=token, verbose=True, overwrite=True)
    except Exception as e:
        assert False, f"osf_upload raised an exception: {e}"

    print("Test passed. File uploaded to OSF.")

    # Cleanup
    os.remove(test_filename)

if __name__ == "__main__":
    test_osf_upload_file()