import os
from miblab import osf_upload

def test_osf_upload_file(local_file):
    """Upload a single file to OSF."""
    assert os.path.isfile(local_file), f"File not found: {local_file}"

    token = os.getenv("OSF_TOKEN")
    assert token, "OSF token not provided. Set the OSF_TOKEN environment variable."

    project_id = "un5ct"
    remote_path = f"Testing/{os.path.basename(local_file)}"

    print(f"Uploading file to OSF at '{remote_path}'")
    try:
        osf_upload(
            local_path=local_file,
            remote_path=remote_path,
            project_id=project_id,
            token=token,
            verbose=True,
            overwrite=True
        )
        print("File upload completed successfully.")
    except Exception as e:
        assert False, f"osf_upload failed: {e}"

if __name__ == "__main__":
    file_path = os.path.expanduser("~/Downloads/OSIPI-DCE Challenge Guidelines_Public.pdf") #Change as appropriate
    assert os.path.isfile(file_path), f"File not found: {file_path}"
    test_osf_upload_file(file_path)