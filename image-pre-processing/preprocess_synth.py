import nibabel as nib
import numpy as np
import os

def pair_synth_files(subject_dir):
    """
    Find matching pairs of synthetic MRI and synthetic labels in a specific subject directory.
    Brain filename structure: *_synth_brain_<idx>_0000.nii.gz
    Label filenames structure: *_synth_labels_<idx>.nii.gz

    :param subject_dir: Directory to a specific subject

    :return:
        A list of synthetic MRI-synthetic labels pairs.
    """
    brains = {}
    labels = {}

    for f in os.listdir(subject_dir):

        # Match the synthetic MRI file name
        if "_synth_brain_" in f:
            part = f.split("_synth_brain_")[1]
            idx = part.split("_")[0]   # take only the first number
            brains[idx] = os.path.join(subject_dir, f)

        # Match the synthetic labels file name
        if "_synth_labels_" in f:
            idx = f.split("_synth_labels_")[1].split(".")[0]
            labels[idx] = os.path.join(subject_dir, f)

    # Find common indices
    common = sorted(set(brains.keys()) & set(labels.keys()))

    pairs = []
    for idx in common:
        pairs.append((brains[idx], labels[idx]))

    return pairs

def synthetic_image_preprocessing(subject_dir, save_path):
    """
    Preprocess synthetic MRI images along with its segmentation mask:
        1. Load segmentation mask
        2. Reorient segmentation mask from LIA to RAS
        3. Extract brain mask merging labels 1, 2 and 3
        4. Load synthetic MRI image
        5. Reorient from LIA to RAS
        6. Apply brain mask to select brain only and remove background
        7. Clip and normalize intensities inside brain
        8. Save outputs

    :param subject_dir: Directory to a specific subject's folder
    :param save_path: Path where the pre-processed images will be saved.

    :return:
        3-D MRI pre-processed to perform image quality assessment
    """

    # Generate list of image pairs in a subject directory
    pairs = pair_synth_files(subject_dir)
    output_paths = []

    for synth_brain_path, synth_label_path in pairs:

        print(f"\nProcessing pair:")
        print(f"  Brain: {synth_brain_path}")
        print(f"  Label: {synth_label_path}")

        # Load segmentation mask
        seg_img = nib.load(synth_label_path)

        # Reorient from LIA to RAS
        seg_ras_img = nib.as_closest_canonical(seg_img)
        seg_data = seg_ras_img.get_fdata()

        # Save re-oriented mask
        base = os.path.basename(synth_label_path)
        seg_name = base.replace(".nii.gz", "_reoriented.nii.gz")
        seg_path = os.path.join(save_path, seg_name)
        seg_out = nib.Nifti1Image(seg_data, seg_ras_img.affine)
        nib.save(seg_out, seg_path)
        print("Saved reoriented mask:", seg_path)

        # Create brain mask merging labels 1, 2 and 3
        brain_labels = [1, 2, 3]
        brain_mask = np.isin(seg_data, brain_labels).astype(np.uint8)

        # Load synthetic MRI
        mri_img = nib.load(synth_brain_path)

        # Reorient from LIA to RAS
        mri_ras_img = nib.as_closest_canonical(mri_img)
        mri_data = mri_ras_img.get_fdata()

        # Apply generated brain mask
        mri_brain = mri_data * brain_mask

        # Normalize
        voxels = mri_brain[brain_mask > 0]

        p1, p99 = np.percentile(voxels, [1, 99])
        mri_brain = np.clip(mri_brain, p1, p99)
        mri_brain = (mri_brain - p1) / (p99 - p1 + 1e-8)

        # Build output path
        base = os.path.basename(synth_brain_path)          # brain_1.nii.gz
        new_name = base.replace(".nii.gz", "_preprocessed.nii.gz")
        out_path = os.path.join(save_path, new_name)

        # Create and save pre-processed image
        out_img = nib.Nifti1Image(mri_brain, mri_ras_img.affine)
        nib.save(out_img, out_path)
        print(f"Saved pre-processed image to {out_path}")
        output_paths.append(out_path)

    return output_paths


def synthetic_mri_preprocessing(dir_path, save_path):
    """
    Walks through all subject folders inside root_dir,
    calls synthetic_image_preprocessing() for each,
    and collects all outputs.

    :param dir_path: Path to directory containing all subject's folders.
    :param save_path: Path where the pre-processed images will be saved.

    :return:
        3-D MRI pre-processed to perform image quality assessment
        Strings updating on pre-processing progress and printing paths to files generated.
    """
    all_outputs = []

    # Iterate through all subjects in directory
    for subject in os.listdir(dir_path):
        subject_path = os.path.join(dir_path, subject)
        print(f"Processing subject: {subject}")

    # Apply pre-processing
        outputs = synthetic_image_preprocessing(subject_path, save_path)
        all_outputs.extend(outputs)

    return "Done!"