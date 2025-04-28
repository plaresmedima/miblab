import os

try:
    import requests
    import_error = False
except:
    import_error = True

try:
    from osfclient.api import OSF
except ImportError:
    OSF = None

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

import zipfile

# Zenodo DOI of the repository
# DOIs need to be updated when new versions are created
DOI = {
    'MRR': "15285017",      # v0.0.3
    'TRISTAN': "15285027"   # v0.0.1
}

# miblab datasets
DATASETS = {
    'KRUK.dmr.zip': {'doi': DOI['MRR']},
    'tristan_humans_healthy_ciclosporin.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_humans_healthy_controls_leeds.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_humans_healthy_controls_sheffield.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_humans_healthy_metformin.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_humans_healthy_rifampicin.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_humans_patients_rifampicin.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_rats_healthy_multiple_dosing.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_rats_healthy_reproducibility.dmr.zip': {'doi': DOI['TRISTAN']},
    'tristan_rats_healthy_six_drugs.dmr.zip': {'doi': DOI['TRISTAN']},
}


def zenodo_fetch(dataset: str, folder: str, doi: str = None, filename: str = None):
    """Download a dataset from Zenodo

    Args:
        dataset (str): Name of the dataset
        folder (str): Local folder where the result is to be saved
        doi (str, optional): Digital object identifier (DOI) of the 
          Zenodo repository where the dataset is uploaded. If this 
          is not provided, the function will look for the dataset in
          miblab's own Zenodo repositories.
        filename (str, optional): Filename of the downloaded dataset. 
          If this is not provided, then *dataset* is used as filename.

    Raises:
        NotImplementedError: If miblab is not installed with the data
          option
        requests.exceptions.ConnectionError: If the connection to 
          Zenodo cannot be made.

    Returns:
        str: Full path to the downloaded datafile.
    """
    if import_error:
        raise NotImplementedError(
            'Please install miblab as pip install miblab[data]'
            ' to use this function.'
        )
    
    # Get DOI
    if doi is None:
        if dataset in DATASETS:
            doi = DATASETS[dataset]['doi']
        else:
            raise ValueError(
                f"{dataset} does not exist in one of the miblab "
                f"repositories on Zenodo. If you want to fetch " 
                f"a dataset in an external Zenodo repository, please "
                f"provide the doi of the repository."
            )
    
    # Dataset download link
    file_url = "https://zenodo.org/records/" + doi + "/files/" + dataset

    # Make the request and check for connection error
    try:
        file_response = requests.get(file_url) 
    except requests.exceptions.ConnectionError as err:
        raise requests.exceptions.ConnectionError(
            f"\n\n"
            f"A connection error occurred trying to download {dataset} "
            f"from Zenodo. This usually happens if you are offline."
            f"The detailed error message is here: {err}"
        ) 
    
    # Check for other errors
    file_response.raise_for_status()

    # Create the folder if needed
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Save the file locally 
    if filename is None:
        file = os.path.join(folder, dataset)
    else:
        file = os.path.join(folder, filename)

    if os.path.exists(file):
        raise ValueError(
            f"Cannot write to {file}. The file already exists. "
            f"Please provide another filename or folder."
        )
        
    with open(file, 'wb') as f:
        f.write(file_response.content)

    return file


def osf_fetch(project_id: str, folder: str, path: list = [], token: str = None, extract: bool = True, verbose: bool = True):
    """Download a dataset from OSF (Open Science Framework)

    Args:
        project_id (str): OSF project ID (e.g., 'un5ct')
        folder (str): Local folder where to save the dataset
        path (list, optional): Subfolders inside project (default empty)
        token (str, optional): Personal OSF token if private access needed
        extract (bool, optional): Whether to unzip .zip files (default True)
        verbose (bool, optional): Whether to print progress (default True)

    Raises:
        ImportError: If osfclient or tqdm not installed
        FileNotFoundError: If folder not found

    Example (public project):
        >>> from miblab.data import osf_fetch
        >>> osf_fetch(
        ...     project_id='un5ct',
        ...     folder='/path/to/save',
        ...     path=['TRISTAN', 'RAT', 'bosentan_highdose', 'Sanofi', 'Day_1']
        ... )

    Example (private project with token):
        >>> from miblab.data import osf_fetch
        >>> osf_fetch(
        ...     project_id='abcde',
        ...     folder='/path/to/save',
        ...     token='your-osf-access-token',
        ...     path=['private', 'dataset', 'folder']
        ... )

    """
    if OSF is None:
        raise ImportError("Please install osfclient: pip install osfclient")
    if tqdm is None:
        raise ImportError("Please install tqdm: pip install tqdm")

    os.makedirs(folder, exist_ok=True)

    osf = OSF(token=token)
    project = osf.project(project_id)
    storage = project.storage('osfstorage')

    current = storage
    for part in path:
        for f in current.folders:
            if f.name == part:
                current = f
                break
        else:
            raise FileNotFoundError(f"Folder '{part}' not found in {'/'.join(path)}")

    def download(current_folder, local_folder):
        os.makedirs(local_folder, exist_ok=True)
        for file in current_folder.files:
            local_file = os.path.join(local_folder, file.name)
            print(f"Downloading {file.name}...")
            try:
                with open(local_file, 'wb') as f:
                    file.write_to(f)
            except Exception as e:
                print(f"Warning downloading {file.name}: {e}")

        for subfolder in current_folder.folders:
            download(subfolder, os.path.join(local_folder, subfolder.name))

    download(current, folder)

    if extract:
        for dirpath, _, filenames in os.walk(folder):
            for filename in filenames:
                if filename.lower().endswith('.zip'):
                    zip_path = os.path.join(dirpath, filename)
                    extract_to = os.path.join(dirpath, filename[:-4])
                    os.makedirs(extract_to, exist_ok=True)
                    try:
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            bad_file = zip_ref.testzip()
                            if bad_file:
                                raise zipfile.BadZipFile(f"Corrupt file {bad_file} inside {zip_path}")
                            zip_ref.extractall(extract_to)
                        os.remove(zip_path)
                        if verbose:
                            print(f"Unzipped and deleted {zip_path}")
                    except Exception as e:
                        if verbose:
                            print(f"Warning unzipping {zip_path}: {e}")

    return folder