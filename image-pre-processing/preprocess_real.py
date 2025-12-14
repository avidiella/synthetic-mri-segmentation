import numpy as np
import nibabel as nib
import os

def zero_pad_to_shape(img, target_shape):
    """
    Zero-pad a 3D image to the target shape, centered.

    :param img: 3D numpy array (H x W x D)
    :param target_shape: tuple (H_t, W_t, D_t)

    :return: padded_img of shape target_shape
    """
    img = np.asarray(img)

    # Create an empty volume filled with zeros
    padded = np.zeros(target_shape, dtype=img.dtype)

    # Compute starting indices
    start = [(t - s) // 2 for s, t in zip(img.shape, target_shape)]

    # Compute ending indices (start + original size)
    end = [start[i] + img.shape[i] for i in range(3)]

    # Fill padded image
    padded[start[0]:end[0],
           start[1]:end[1],
           start[2]:end[2]] = img

    return padded


def real_mri_preprocessing(dir_path, save_path, target_shape=(256, 256, 256)):
    """
    Preprocess a real MRI:
    1. Load real MRI 3-D image
    2. Zero-pad to target shape (256x256x256)
    3. Extract brain mask
    4. Clip and normalize intensities inside brain

    :param dir_path: Directory with subject's folders.
    :param save_path: Path where the pre-processed images will be saved.
    :param target_shape: Target shape for new image (always 256x256x256)

    :return:
        3-D MRI pre-processed to perform image quality assessment
    """
    # Walk the real MRI directory
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            # Identify stripped nii.gz files
            if file.endswith("_stripped.nii.gz"):
                # Generate argument --img_path
                img_path = os.path.join(root, file)

                # Load image
                img = nib.load(img_path)
                data = img.get_fdata()

                # Zero-padding to match target shape
                real_padded = zero_pad_to_shape(data, target_shape)

                # Extract brain mask
                threshold = np.percentile(real_padded, 1)
                brain_mask = real_padded > threshold

                # Clip and normalize intensities inside brain
                p1 = np.percentile(real_padded[brain_mask], 1)
                p99 = np.percentile(real_padded[brain_mask], 99)

                real_norm = np.clip(real_padded, p1, p99)
                real_norm = (real_norm - p1) / (p99 - p1)

                # Build new filename
                orig_name = os.path.basename(img_path)
                name_no_ext = orig_name.replace(".nii.gz", "").replace(".nii", "")
                new_name = name_no_ext + "_preprocessed.nii.gz"

                # Final save path
                final_path = os.path.join(save_path, new_name)

                # Save
                norm_img = nib.Nifti1Image(real_norm, img.affine)
                nib.save(norm_img, final_path)

                print(f"Saved pre-processed image to {final_path}")