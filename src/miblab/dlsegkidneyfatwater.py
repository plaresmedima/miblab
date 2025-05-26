import os
import sys
import numpy as np
from miblab.data import zenodo_fetch
from miblab.data import clear_cache_datafiles
import scipy.ndimage as ndi
import nibabel as nib

if sys.version_info < (3, 9):
    # importlib.resources either doesn't exist or lacks the files()
    # function, so use the PyPI version:
    import importlib_resources
else:
    # importlib.resources has files(), so use that:
    import importlib.resources as importlib_resources

try:
    from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor
    nnunetv2 = True

except ImportError:
    nnunetv2 = False

try:
    import torch
    torch_installed = True
except ImportError:
    torch_installed = False

MODEL = 'nnunet_kidney_fatwater_v1.zip'
MODEL_DOI = "15356746"

def kidney_dixon_fat_water(input_array, clear_cache = False, verbose=False):
    
    """
    Calculate fat/water maps on post-contrast Dixon images.
     
    This requires 2-channel input data with out-phase images, 
    in-phase images.

    This uses a pretrained nnunet based model, hosted on 
    `Zenodo <https://zenodo.org/records/15356746>`_

    Args:
        input_array (numpy.ndarray): A 4D numpy array of shape 
            [x, y, z, contrast] representing the input medical image 
            volume. The last index must contain out-phase, in-phase, 
            water and fat images, in that order.
        clear_cache: If True, the downloaded pth file is removed 
            again after running the inference.
        verbose (bool): If True, prints logging messages.

    Returns:
        dict: 
            A dictionary with the keys 'fatmap' and 
            'watermap', each containing a binary NumPy array 
            representing the respective kidney mask.
    Example:

        >>> import numpy as np
        >>> import miblab
        >>> data = np.random.rand((128, 128, 30, 4))
        >>> mask = miblab.kidney_pc_dixon(data)
        >>> print(mask['leftkidney'])
        [0 1 1 ... 0 0 0]
    """
    if not torch_installed:
        raise ImportError(
            'torch is not installed. Please install it with "pip install torch".'
            'To install all dlseg options at once, install miblab as pip install miblab[dlseg].'
        )
    if not nnunetv2:
        raise ImportError(
            'nnunetv2 is not installed. Please install it with "pip install nnunetv2".'
            'To install all dlseg options at once, install miblab as pip install miblab[dlseg].'
        )

    if verbose:
        print('Downloading model..')

    temp_dir = importlib_resources.files('miblab.datafiles')
    weights_path = zenodo_fetch(MODEL, temp_dir, MODEL_DOI,extract=True)

    if verbose:
        print('Applying model to data..')

    # Setup device
    predictor = nnUNetPredictor(
        tile_step_size=0.75,
        use_gaussian=True,
        use_mirroring=False,
        perform_everything_on_device=True,
        device=torch.device('cpu'),
        verbose=False,
        verbose_preprocessing=False,
        allow_tqdm=True)

    nested_folder = os.path.join(weights_path, "nnUNetTrainer__nnUNetPlans__3d_fullres")

    predictor.initialize_from_trained_model_folder(
    nested_folder,
    use_folds='3',
    checkpoint_name='checkpoint_best.pth'
    )

    temp_folder_results = os.path.join(temp_dir,"temp_results")
    temp_folder_data_to_test = os.path.join(temp_dir,"temp_results",'data_to_test')
    os.makedirs(temp_folder_data_to_test, exist_ok=True)

    affine = np.eye(4)
    nii_out_ph = nib.Nifti1Image(input_array[...,0], affine) # minus in the third column
    nib.save(nii_out_ph, os.path.join(temp_folder_data_to_test, 'Dixon_999_0000.nii.gz'))
    nii_in_ph = nib.Nifti1Image(input_array[...,1], affine)
    nib.save(nii_in_ph, os.path.join(temp_folder_data_to_test, 'Dixon_999_0001.nii.gz'))

    predictor.predict_from_files(temp_folder_data_to_test,temp_folder_results, 
    save_probabilities=False, 
    overwrite=True)

    # Load the NIfTI file
    nifti_file = nib.load(os.path.join(temp_folder_results,'Dixon_999.nii.gz'))

    array_Dixon_water_dom = nifti_file.get_fdata()

    array_water_calculated = np.zeros_like(input_array[...,0])  # Ensure same shape
    array_water_calculated = np.where(array_Dixon_water_dom == 1, input_array[...,1] + input_array[...,0], array_water_calculated)
    array_water_calculated = np.where(array_Dixon_water_dom == 0, input_array[...,1] - input_array[...,0], array_water_calculated)

    array_fat_calculated = np.zeros_like(input_array[...,0])  # Ensure same shape
    array_fat_calculated = np.where(array_Dixon_water_dom == 0, input_array[...,1] + input_array[...,0], array_fat_calculated)
    array_fat_calculated = np.where(array_Dixon_water_dom == 1, input_array[...,1] - input_array[...,0], array_fat_calculated)

    if clear_cache:
        if verbose:
            print('Deleting downloaded files...')
        clear_cache_datafiles(temp_dir)


    fatwatermap = {
        "fatmap": array_fat_calculated,
        "watermap": array_water_calculated
    }

    return fatwatermap