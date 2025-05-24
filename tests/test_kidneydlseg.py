import dbdicom as db
import numpy as np

from miblab import kidney_pc_dixon
from miblab import zenodo_fetch

import os
 

def test_kidney_pc_dixon():
    
    temp_dir = os.path.join(os.path.dirname(__file__), 'datafiles')

    testdata = 'test_data_post_contrast_dixon.zip'
    testdatadoi = '15489381'

    # Download ZIP file to temp directory
    zenodo_fetch(testdata, temp_dir, testdatadoi,extract=True)

    # Load DICOM database
    database = db.database(path=os.path.join(temp_dir,'test_data_post_contrast_dixon'))

    series_outphase = database.series(SeriesDescription='Dixon_post_contrast_out_phase')
    series_inphase = database.series(SeriesDescription='Dixon_post_contrast_in_phase')
    series_water = database.series(SeriesDescription='Dixon_post_contrast_water')
    series_fat = database.series(SeriesDescription='Dixon_post_contrast_fat')

    array_outphase, _ = series_outphase[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_inphase, _ = series_inphase[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_water, _ = series_water[0].array(['SliceLocation'], pixels_first=True, first_volume=True)
    array_fat, _ = series_fat[0].array(['SliceLocation'], pixels_first=True, first_volume=True)

    array = np.stack((array_outphase, array_inphase, array_water, array_fat), axis=3)

    mask = kidney_pc_dixon(array)

    assert np.sum(mask['leftkidney']) == 62284#

