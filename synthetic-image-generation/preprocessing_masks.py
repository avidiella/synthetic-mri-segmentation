import os
import numpy as np
import nibabel as nib

def convert_freesurfer_masks(file_mask):
    """
    Preprocess a FreeSurfer `aparc+aseg.mgz` segmentation mask and generate a
    3-class tissue segmentation (GM=1, WM=2, CSF=3).

    The function loads the input NIfTI/MGZ mask, groups anatomical labels into
    gray matter, white matter, and cerebrospinal fluid, and saves a new file
    called `processed_mask.nii.gz` in the same directory.

    :param file_mask: The whole path to file `aparc+aseg.mgz`.
    :return: Prints progress messages for each processed file and full path of the saved processed mask.
    """
    # Get aparc+aseg.mgz file
    img = nib.load(file_mask)
    data = img.get_fdata().astype(int)

    # Group labels according to segmentation dictionary
    gm_labels = [8, 10, 11, 12, 13, 17, 18, 26, 28, 31, 47, 49, 50, 51, 52, 53, 54, 58, 60,
                 63, 80, 1000, 1001, 1002, 1003, 1005, 1006, 1007, 1008, 1009, 1010, 1011,
                 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024,
                 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 2000, 2001,
                 2002, 2003, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015,
                 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028,
                 2029, 2030, 2031, 2032, 2033, 2034, 2035]
    wm_labels = [2, 7, 16, 41, 46, 77, 85, 251, 252, 253, 254, 255]
    csf_labels = [4, 5, 14, 15, 24, 43, 44, 72]

    # Create mask
    gm_mask = np.isin(data, gm_labels)
    wm_mask = np.isin(data, wm_labels)
    csf_mask = np.isin(data, csf_labels)

    # Combine into 1 volume
    tissue_volume = np.zeros_like(data, dtype=np.uint8)
    tissue_volume[gm_mask] = 1
    tissue_volume[wm_mask] = 2
    tissue_volume[csf_mask] = 3

    # Save NIfTI
    tissue_img = nib.Nifti1Image(tissue_volume, img.affine)
    nib.save(tissue_img, os.path.join(os.path.split(file_mask)[0], "processed_mask.nii.gz"))
    print(f"A preprocessed segmentation mask was saved in {os.path.join(os.path.split(file_mask)[0], 'processed_mask.nii.gz')}.")

def process_masks(subjects_dir):
    """
    Scan the dataset directory and preprocess all segmentation masks.

    This function assumes the default file hierarchy in Freesurfer project
    and searches inside `subjects_dir`, locates all subfolders `mri` that
    contain a FreeSurfer segmentation at `mri/aparc+aseg.mgz`, and applies
    function `preprocessing_masks()` to each one.

    :param subjects_dir: A standard FreeSurfer subject directory.
    :return: Prints progress messages for each processed file.
    """
    # Create list with every subject directory
    inventory_list = os.listdir(subjects_dir)

    # Iterate through all subjects and create preprocessed mask
    for i in inventory_list:
        dirs = os.path.join(subjects_dir + "\\" + i + r"\mri\aparc+aseg.mgz")
        convert_freesurfer_masks(dirs)